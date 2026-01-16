"""Configuration loader for environment variables."""

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(
        env_file=".env", case_sensitive=False, populate_by_name=True
    )

    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="password", alias="NEO4J_PASSWORD")

    # Logfire Configuration
    logfire_token: str | None = Field(default=None, alias="LOGFIRE_TOKEN")
    logfire_project_name: str = Field(
        default="P_S_CQC_companion", alias="LOGFIRE_PROJECT_NAME"
    )

    # Application Configuration
    env: str = Field(default="development", alias="ENV")
    debug: bool = Field(default=True, alias="DEBUG")


settings = Settings()
