import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class MentalHealthChatbot:
    def __init__(self, data_dir="data", model_name="llama3.2:1b"):
        self.data_dir = data_dir
        self.model_name = model_name
        self.vector_store = None
        self.retriever = None
        self.chain = None
        
        # Initialize LLM
        print(f"Initializing Ollama model command: {model_name}...")
        self.llm = OllamaLLM(model=model_name, streaming=True)
        
        # Initialize Embeddings
        print("Initializing Embeddings (all-MiniLM-L6-v2)...")
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Load or Create Vector Store
        self.index_path = "faiss_index"
        if os.path.exists(self.index_path):
            print("Loading existing FAISS index...")
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            self.create_chain()
        else:
            print("No index found. Please ingest documents first.")

    def ingest_docs(self):
        print(f"Loading documents from {self.data_dir}...")
        
        # Load TXT files
        txt_loader = DirectoryLoader(self.data_dir, glob="**/*.txt", loader_cls=TextLoader)
        txt_docs = txt_loader.load()
        
        # Load PDF files (if any)
        try:
            pdf_loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
            pdf_docs = pdf_loader.load()
        except Exception as e:
            print(f"Error loading PDFs: {e}")
            pdf_docs = []
        
        documents = txt_docs + pdf_docs
        
        if not documents:
            print("No documents found to ingest.")
            return "No documents found."
            
        print(f"Loaded {len(documents)} documents. Splitting text...")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)
        
        print(f"Created {len(chunks)} chunks. Creating vector store...")
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.vector_store.save_local(self.index_path)
        
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        self.create_chain()
        print("Ingestion complete.")
        return "Ingestion complete."

    def create_chain(self):
        template = """
        You are a compassionate and empathetic mental health AI assistant. 
        Your goal is to provide supportive, non-judgmental, and helpful responses.
        
        {mood_context}
        {language_instruction}
        
        Use the following context to answer the user's question. 
        If the context doesn't contain the answer, use your general knowledge to provide a supportive response, 
        BUT always prioritize the context if relevant.
        
        STORYTELLING/DISTRACTION: If the user asks for a story, anecdote, or distraction, tell a short (2-3 paragraph), 
        uplifting, and motivational story. Focus on themes of resilience, hope, or finding peace in small moments.
        
        If the user expresses thoughts of self-harm or suicide, IMMEDIATELEY provide crisis helpline information 
        and urge them to seek professional help. Do not try to diagnose or treat serious conditions yourself.
        
        Context: {context}
        
        User Question: {question}
        
        Answer (Be very concise, use simple words, and limit response to few lines):
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question", "mood_context", "language_instruction"]
        )
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.chain = (
            {
                "context": lambda x: format_docs(self.retriever.invoke(x["question"])), 
                "question": lambda x: x["question"], 
                "mood_context": lambda x: x.get("mood_context", ""),
                "language_instruction": lambda x: x.get("language_instruction", "")
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def get_response(self, query, mood=None, language="English"):
        if not self.chain:
            return "System is not ready. Please ingest data first."
        
        # Create mood context if mood is provided
        mood_context = ""
        if mood:
            mood_descriptions = {
                'happy': "The user appears to be in a positive mood.",
                'sad': "The user appears to be feeling sad or down. Be extra empathetic and supportive.",
                'angry': "The user appears to be frustrated or angry. Be calm, understanding, and non-judgmental.",
                'fear': "The user appears to be anxious or worried. Be reassuring and gentle.",
                'neutral': "The user appears to be in a neutral, calm state.",
                'surprise': "The user appears to be surprised.",
                'disgust': "The user appears to be uncomfortable or bothered by something. Be understanding."
            }
            mood_context = mood_descriptions.get(mood, "")
        
        # Create language instruction
        lang_instruction = f"IMPORTANT: You MUST respond in {language}. Use simple words only. Do not use complex sentences. Keep the response to 2-4 short lines only."
        if language != "English":
            lang_instruction += f" Ensure the translation to {language} is natural and empathetic."
        
        try:
            # Invoking the LCEL chain with mood and language context
            response = self.chain.invoke({
                "question": query, 
                "mood_context": mood_context,
                "language_instruction": lang_instruction
            })
            return response
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_journal_summary(self, entries: list) -> str:
        """Generates a concise, insightful summary of multiple journal entries."""
        if not entries:
            return "No entries yet this week. Start writing to see your emotional patterns!"
            
        combined_text = "\n---\n".join([e['entry_text'] for e in entries])
        prompt = f"""
        Analyze the following journal entries from this week and provide a concise (2-3 sentence) summary.
        Identify emotional patterns, key highlights, and provide a tiny piece of encouragement.
        
        Entries:
        {combined_text}
        
        Summary:
        """
        try:
            return self.llm.invoke(prompt).strip()
        except:
            return "Unable to generate summary at this time, but your growth is showing!"

    def get_response_stream(self, query, mood=None, language="English"):
        """Streams the response chunk by chunk for better perceived performance."""
        if not self.chain:
            yield "System is not ready."
            return

        mood_context = ""
        if mood:
            mood_descriptions = {
                'happy': "The user appears to be in a positive mood.",
                'sad': "The user appears to be feeling sad or down. Be extra empathetic and supportive.",
                'angry': "The user appears to be frustrated or angry. Be calm, understanding, and non-judgmental.",
                'fear': "The user appears to be anxious or worried. Be reassuring and gentle.",
                'neutral': "The user appears to be in a neutral, calm state.",
            }
            mood_context = mood_descriptions.get(mood, "")

        # Create language instruction
        lang_instruction = f"IMPORTANT: You MUST respond in {language}. Use simple words only. Keep it very short (max 3 lines)."

        try:
            for chunk in self.chain.stream({
                "question": query, 
                "mood_context": mood_context,
                "language_instruction": lang_instruction
            }):
                yield chunk
        except Exception as e:
            yield f"\n[Error streaming: {str(e)}]"

if __name__ == "__main__":
    # Test run
    bot = MentalHealthChatbot()
    if not os.path.exists("faiss_index"):
        bot.ingest_docs()
    
    print("\nTest Response:")
    print(bot.get_response("I honestly feel very overwhelmed with work lately."))
