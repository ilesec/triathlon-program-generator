from pydantic_settings import BaseSettings
from pydantic import Field, AliasChoices
from typing import Optional


class Settings(BaseSettings):
    # LLM Provider: "anthropic" or "azure_ai"
    llm_provider: str = Field(
        default="anthropic",
        validation_alias=AliasChoices("LLM_PROVIDER", "llm_provider"),
    )
    
    # Anthropic settings
    anthropic_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "ANTHROPIC_API_KEY",
            "CLAUDE_API_KEY",
            "anthropic_api_key",
        ),
    )
    
    # Azure AI Studio settings
    azure_ai_endpoint: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "AZURE_AI_ENDPOINT",
            "AZURE_OPENAI_ENDPOINT",
            "azure_ai_endpoint",
        ),
    )
    azure_ai_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "AZURE_AI_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_KEY",
            "azure_ai_api_key",
        ),
    )
    azure_ai_deployment_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "AZURE_AI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_DEPLOYMENT_NAME",
            "AZURE_OPENAI_DEPLOYMENT",
            "azure_ai_deployment_name",
        ),
    )
    azure_ai_api_version: str = Field(
        default="2024-02-15-preview",
        validation_alias=AliasChoices(
            "AZURE_AI_API_VERSION",
            "AZURE_OPENAI_API_VERSION",
            "azure_ai_api_version",
        ),
    )
    # Azure AI auth mode: "api_key" or "entra_id" (Managed Identity / Entra ID)
    azure_ai_auth: str = Field(
        default="api_key",
        validation_alias=AliasChoices(
            "AZURE_AI_AUTH",
            "AZURE_OPENAI_AUTH",
            "azure_ai_auth",
        ),
    )
    # For user-assigned managed identity (optional). Leave empty for system-assigned.
    azure_ai_managed_identity_client_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "AZURE_AI_MANAGED_IDENTITY_CLIENT_ID",
            "AZURE_OPENAI_MANAGED_IDENTITY_CLIENT_ID",
            "azure_ai_managed_identity_client_id",
        ),
    )
    
    # Database
    database_url: str = "sqlite:///./workouts.db"
    
    class Config:
        env_file = ".env"


settings = Settings()
