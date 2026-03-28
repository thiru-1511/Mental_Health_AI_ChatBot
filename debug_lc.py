import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Path: {sys.path}")

try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    print(f"LangChain file: {langchain.__file__}")
    print(f"LangChain dir: {os.path.dirname(langchain.__file__)}")
    print(f"Contents of langchain dir: {os.listdir(os.path.dirname(langchain.__file__))}")
    
    try:
        import langchain.chains
        print("Successfully imported langchain.chains")
    except ImportError as e:
        print(f"Failed to import langchain.chains: {e}")

except ImportError as e:
    print(f"Failed to import langchain: {e}")

try:
    import langchain_community
    print(f"LangChain Community version: {langchain_community.__version__}")
except ImportError:
    print("LangChain Community not found")
