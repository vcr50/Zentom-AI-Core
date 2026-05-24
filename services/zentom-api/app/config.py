from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    ai_mode: str = Field(default="RULE", alias="AI_MODE")
    ai_provider: str = Field(default="LOCAL", alias="AI_PROVIDER")
    ai_api_key: str | None = Field(default=None, alias="AI_API_KEY")
    ai_model: str = Field(default="zentom-rule-v1", alias="AI_MODEL")
    local_llm_url: str = Field(default="http://localhost:11434", alias="LOCAL_LLM_URL")
    local_llm_model: str = Field(default="llama3.1:8b", alias="LOCAL_LLM_MODEL")
    embedding_model: str = Field(default="all-minilm", alias="EMBEDDING_MODEL")
    zentom_api_key: str | None = Field(default=None, alias="ZENTOM_API_KEY")

    @property
    def AI_MODE(self) -> str:
        return self.ai_mode

    @property
    def AI_PROVIDER(self) -> str:
        return self.ai_provider

    @property
    def AI_API_KEY(self) -> str | None:
        return self.ai_api_key

    @property
    def AI_MODEL(self) -> str:
        return self.ai_model

    @property
    def LOCAL_LLM_URL(self) -> str:
        return self.local_llm_url

    @property
    def LOCAL_LLM_MODEL(self) -> str:
        return self.local_llm_model

    @property
    def EMBEDDING_MODEL(self) -> str:
        return self.embedding_model

    @property
    def ZENTOM_API_KEY(self) -> str | None:
        return self.zentom_api_key

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
