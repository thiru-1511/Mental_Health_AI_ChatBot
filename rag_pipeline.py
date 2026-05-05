import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Google Gemini API Setup ---
# Set GOOGLE_API_KEY as an environment variable on Render dashboard
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

class MentalHealthChatbot:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.vector_store = None
        self.retriever = None
        self.chain = None

        if not GOOGLE_API_KEY:
            print("WARNING: GOOGLE_API_KEY is not set. Chat responses will be limited.")
            self.llm = None
            self.embeddings = None
        else:
            # Lightweight: uses Gemini API — no local model loaded into RAM
            print("Initializing Google Gemini LLM (gemini-1.5-flash)...")
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.7,
                streaming=True
            )
            print("Initializing Google Gemini Embeddings...")
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=GOOGLE_API_KEY
            )

        # Load or Create Vector Store
        self.index_path = "faiss_index"
        if self.embeddings and os.path.exists(self.index_path):
            print("Loading existing FAISS index...")
            try:
                self.vector_store = FAISS.load_local(
                    self.index_path, self.embeddings, allow_dangerous_deserialization=True
                )
                self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
                self.create_chain()
            except Exception as e:
                print(f"Warning: Could not load FAISS index: {e}. Will run without RAG.")
        else:
            print("No FAISS index found. Chatbot will rely on Gemini's built-in knowledge.")

    def ingest_docs(self):
        if not self.embeddings:
            return "Cannot ingest: GOOGLE_API_KEY not set."

        print(f"Loading documents from {self.data_dir}...")
        txt_loader = DirectoryLoader(self.data_dir, glob="**/*.txt", loader_cls=TextLoader)
        txt_docs = txt_loader.load()

        try:
            pdf_loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
            pdf_docs = pdf_loader.load()
        except Exception as e:
            print(f"Error loading PDFs: {e}")
            pdf_docs = []

        documents = txt_docs + pdf_docs
        if not documents:
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
        if not self.llm:
            return

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

        If the user expresses thoughts of self-harm or suicide, IMMEDIATELY provide crisis helpline information
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

        if self.retriever:
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
        else:
            # No RAG — direct LLM with just prompt (no context)
            simple_template = """
            You are a compassionate and empathetic mental health AI assistant.
            {mood_context}
            {language_instruction}
            User Question: {question}
            Answer (Be very concise, use simple words, and limit response to few lines):
            """
            simple_prompt = PromptTemplate(
                template=simple_template,
                input_variables=["question", "mood_context", "language_instruction"]
            )
            self.chain = (
                {
                    "question": lambda x: x["question"],
                    "mood_context": lambda x: x.get("mood_context", ""),
                    "language_instruction": lambda x: x.get("language_instruction", "")
                }
                | simple_prompt
                | self.llm
                | StrOutputParser()
            )

    def _build_inputs(self, query, mood=None, language="English"):
        mood_descriptions = {
            'happy': "The user appears to be in a positive mood.",
            'sad': "The user appears to be feeling sad or down. Be extra empathetic and supportive.",
            'angry': "The user appears to be frustrated or angry. Be calm, understanding, and non-judgmental.",
            'fear': "The user appears to be anxious or worried. Be reassuring and gentle.",
            'neutral': "The user appears to be in a neutral, calm state.",
            'surprise': "The user appears to be surprised.",
            'disgust': "The user appears to be uncomfortable or bothered by something. Be understanding."
        }
        mood_context = mood_descriptions.get(mood, "") if mood else ""
        lang_instruction = (
            f"IMPORTANT: You MUST respond in {language}. Use simple words only. "
            f"Do not use complex sentences. Keep the response to 2-4 short lines only."
        )
        if language != "English":
            lang_instruction += f" Ensure the translation to {language} is natural and empathetic."
        return {"question": query, "mood_context": mood_context, "language_instruction": lang_instruction}

    def get_response(self, query, mood=None, language="English"):
        if not self.chain:
            if not GOOGLE_API_KEY:
                return "Chat is unavailable: the server is not configured with an AI key. Please contact the administrator."
            return "System is initializing. Please try again in a moment."

        try:
            response = self.chain.invoke(self._build_inputs(query, mood, language))
            return response
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_journal_summary(self, entries: list) -> str:
        if not self.llm:
            return "AI summary unavailable. Please configure the API key."
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
            return self.llm.invoke(prompt).content.strip()
        except:
            return "Unable to generate summary at this time, but your growth is showing!"

    def get_response_stream(self, query, mood=None, language="English"):
        """Streams the response chunk by chunk for better perceived performance."""
        if not self.chain:
            yield "Chat is unavailable: the server is not configured with an AI key."
            return

        try:
            for chunk in self.chain.stream(self._build_inputs(query, mood, language)):
                yield chunk
        except Exception as e:
            yield f"\n[Error streaming: {str(e)}]"


if __name__ == "__main__":
    bot = MentalHealthChatbot()
    if not os.path.exists("faiss_index"):
        bot.ingest_docs()
    print("\nTest Response:")
    print(bot.get_response("I honestly feel very overwhelmed with work lately."))
