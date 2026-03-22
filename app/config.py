from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 8000
    cors_origins: str = "*"

    pinecone_api_key: str
    pinecone_index: str = "resume-chatbot"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    openrouter_api_key: str
    openrouter_model: str = "deepseek/deepseek-chat"
    openrouter_site_url: str | None = None
    openrouter_app_name: str | None = None

    top_k: int = 5
    max_context_chars: int = 12000

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
