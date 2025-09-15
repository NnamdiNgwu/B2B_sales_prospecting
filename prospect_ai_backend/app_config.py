# In this file, you can set the configurations of the app.
from __future__ import annotations

import os
import sys
import json
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Literal

from loguru import logger
from pydantic import Field, field_validator, AliasChoices, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # optional

# ---- Logging (console + JSON file) ----
ROOT_DIR = Path(__file__).parent
LOG_DIR = ROOT_DIR / "log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MIN_LOG_LEVEL = os.getenv("MINIMUM_LOG_LEVEL", "DEBUG").upper()

logger.remove()  # clear defaults
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> "
           "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
           "- <level>{message}</level>",
    level=MIN_LOG_LEVEL,
)
logger.add(LOG_DIR / "app.log", serialize=True, level="INFO", rotation="10 MB", retention="10 days", compression="zip")

DATA_DIR = ROOT_DIR / "data_folder"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONTACT_CFG_PATH = DATA_DIR / "contact_form_config.yaml"


class AppConfig(BaseSettings):
    # App
    app_name: str = Field(default="Prospect AI Backend", env="APP_NAME")
    environment: str = Field(default=os.getenv("ENV", "development"), env="ENV")
    debug: bool = Field(default=os.getenv("DEBUG", "false").lower() == "true", env="DEBUG")
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "CHANGE_ME"), env="SECRET_KEY")

    # Backend I/O
    database_url: Optional[str] = Field(default=os.getenv("DATABASE_URL"), env="DATABASE_URL")
    celery_broker_url: str = Field(default=os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"), env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default=os.getenv("CELERY_RESULT_BACKEND", os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")), env="CELERY_RESULT_BACKEND")

    # CORS
    cors_origins: List[str] = Field(default=["http://localhost:5173", "http://127.0.0.1:5173"], env="CORS_ORIGINS")

    # Vector/LLM/Qdrant
    qdrant_host: str = Field(default=os.getenv("QDRANT_HOST", "localhost"), env="QDRANT_HOST")
    qdrant_port: int = Field(default=int(os.getenv("QDRANT_PORT", "7543")), env="QDRANT_PORT")
    qdrant_collection: str = Field(default=os.getenv("QDRANT_COLLECTION", "vulnerabilities"), env="QDRANT_COLLECTION")
    embedding_model: str = Field(default=os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest"), env="EMBEDDING_MODEL")
    llm_model: str = Field(default=os.getenv("LLM_MODEL", "groq/llama3-groq-70b-8192-tool-use-preview"), env="LLM_MODEL")

    # Provider selection and credentials
    llm_model_type: Literal["openai", "groq", "ollama"] = Field(default=os.getenv("LLM_MODEL_TYPE", "openai"), env="LLM_MODEL_TYPE")
    llm_api_url: Optional[str] = Field(default=os.getenv("LLM_API_URL"), env="LLM_API_URL")  # used for ollama/self-hosted
    groq_api_key: Optional[SecretStr] = Field(default=None, validation_alias=AliasChoices("GROQ_API_KEY"))
    openai_api_key: Optional[SecretStr] = Field(default=None, validation_alias=AliasChoices("OPENAI_API_KEY", "OPENAI_KEY"))

    vector_size: int = Field(default=int(os.getenv("VECTOR_SIZE", "768")), env="VECTOR_SIZE")
    search_k: int = Field(default=int(os.getenv("SEARCH_K", "5")), env="SEARCH_K")

    # Contact form campaign controls (merged with YAML if present)
    contact_output_dir: Path = Field(default=Path(os.getenv("CONTACT_OUTPUT_DIR", DATA_DIR / "output" / "contact_submissions")))
    contact_delay_seconds: int = Field(default=int(os.getenv("CONTACT_DELAY_SECONDS", "30")))
    max_submissions_per_hour: int = Field(default=int(os.getenv("MAX_SUBMISSIONS_PER_HOUR", "20")))
    respect_robots_txt: bool = Field(default=os.getenv("RESPECT_ROBOTS_TXT", "true").lower() == "true")
    contact_config_path: Path = Field(default=Path(os.getenv("CONTACT_CONFIG_PATH", DEFAULT_CONTACT_CFG_PATH)))

    # Optional strictness toggle for provider creds
    require_llm_creds: bool = Field(default=os.getenv("REQUIRE_LLM_CREDS", "false").lower() == "true", env="REQUIRE_LLM_CREDS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("qdrant_port", "vector_size", "search_k", "contact_delay_seconds", "max_submissions_per_hour")
    @classmethod
    def non_negative_ints(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Numeric fields must be non-negative.")
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            # Accept JSON array or CSV
            try:
                loaded = json.loads(v)
                if isinstance(loaded, list):
                    return loaded
            except Exception:
                pass
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    def merge_contact_yaml(self) -> None:
        """Overlay values from contact_form_config.yaml if present (non-destructive)."""
        try:
            if self.contact_config_path and self.contact_config_path.exists() and yaml is not None:
                data = yaml.safe_load(self.contact_config_path.read_text(encoding="utf-8")) or {}
                # top-level controls
                self.contact_delay_seconds = int(data.get("delay_between_submissions", self.contact_delay_seconds))
                self.max_submissions_per_hour = int(data.get("max_submissions_per_hour", self.max_submissions_per_hour))
                self.respect_robots_txt = bool(data.get("respect_robots_txt", self.respect_robots_txt))
                out_dir = data.get("outputFileDirectory")
                if out_dir:
                    self.contact_output_dir = Path(out_dir)
        except Exception as e:
            logger.warning(f"Failed to merge contact YAML config: {e}")

    def ensure_dirs(self) -> None:
        try:
            self.contact_output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create output dir {self.contact_output_dir}: {e}")

    def redact(self) -> dict:
        """Return a dict suitable for logs with secrets masked."""
        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "debug": self.debug,
            "database_url": ("***" if self.database_url else None),
            "celery_broker_url": self.celery_broker_url,
            "celery_result_backend": self.celery_result_backend,
            "cors_origins": self.cors_origins,
            "llm_model_type": self.llm_model_type,
            "llm_model": self.llm_model,
            "llm_api_url": self.llm_api_url,
            "openai_api_key": "***" if self.openai_api_key else None,
            "groq_api_key": "***" if self.groq_api_key else None,
            "vector_size": self.vector_size,
            "search_k": self.search_k,
            "contact_output_dir": str(self.contact_output_dir),
            "contact_delay_seconds": self.contact_delay_seconds,
            "max_submissions_per_hour": self.max_submissions_per_hour,
            "respect_robots_txt": self.respect_robots_txt,
        }

    # Soft validation: warn (or error) if required creds for selected provider are missing
    @field_validator("llm_model_type", mode="after")
    @classmethod
    def _warn_missing_provider_creds(cls, v, info):
        # info.data contains already-parsed fields
        data = info.data if hasattr(info, "data") else {}
        require = bool(data.get("require_llm_creds", False))
        provider = v
        missing = []
        if provider == "openai":
            if not data.get("openai_api_key"):
                missing.append("OPENAI_API_KEY")
        elif provider == "groq":
            if not data.get("groq_api_key"):
                missing.append("GROQ_API_KEY")
        elif provider == "ollama":
            if not data.get("llm_api_url"):
                missing.append("LLM_API_URL")
        if missing:
            msg = f"LLM provider '{provider}' missing config: {', '.join(missing)}"
            if require:
                raise ValueError(msg)
            logger.warning(msg)
        return v


@lru_cache
def get_settings() -> AppConfig:
    # Optional .env loading via pydantic; also honor legacy config.env
    cfg = AppConfig()
    # Legacy "config.env" support
    config_env = ROOT_DIR / "config.env"
    if config_env.exists():
        for line in config_env.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().replace('"', "")
        cfg = AppConfig()  # re-load with updated env
    cfg.merge_contact_yaml()
    cfg.ensure_dirs()
    logger.debug(f"Loaded settings: {cfg.redact()}")
    return cfg


# ---- Backwards-compatible classes (optional) ----

class Config:
    APP_NAME = os.getenv("APP_NAME", "Prospect AI Backend")
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
    OPENAI_KEY = os.getenv("OPENAI_KEY")

    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    @classmethod
    def init_app(cls):
        logger.info("App in DEVELOPMENT mode")


class TestingConfig(Config):
    TEST = True

    @classmethod
    def init_app(cls):
        logger.info("App in TESTING mode")


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls):
        logger.info("App in PRODUCTION mode")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

# Public, importable singleton
settings = get_settings()


"""
MINIMUM_LOG_LEVEL can only be one of the followings:
    - "DEBUG"
    - "INFO"
    - "WARNING"
    - "ERROR"
    - "CRITICAL"
"""
MINIMUM_LOG_LEVEL = MIN_LOG_LEVEL  # keep backwards-compat with callers

MINIMUM_WAIT_TIME = 60