import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from utils.config_loader import load_config
from langchain_groq import ChatGroq

class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()

    def _validate_env(self):
        """
        Validate necessary environment variables.
        """
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY"]
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
    def load_embeddings(self):
        """
        Load and return the embedding model based on the configuration.
        """
        print("Loading Embedding model")
        provider = self.config["embedding_model"]["provider"].lower()
        model_name = self.config["embedding_model"]["model_name"]
        if provider == "google":
            return GoogleGenerativeAIEmbeddings(model=model_name, api_key=self.google_api_key)
        elif provider == "openai":
            return OpenAIEmbeddings(model=model_name, api_key=self.openai_api_key)
        else:
            raise ValueError(f"Unsupported embedding model: {model_name}")
        
    def load_llm(self):
        """
        Load and return the LLM model based on the configuration.
        """
        print("Loading LLM model")
        provider = self.config["llm"]["provider"].lower()
        model_name = self.config["llm"]["model_name"]
        if provider == "groq":
            return ChatGroq(model=model_name, api_key=self.groq_api_key)
        elif provider == "google":
            return ChatGoogleGenerativeAI(model=model_name)
        elif provider == "openai":
            return ChatOpenAI(model=model_name, api_key=self.openai_api_key)
        else:
            raise ValueError(f"Unsupported LLM model: {model_name}")