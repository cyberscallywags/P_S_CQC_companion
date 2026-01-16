"""Logging configuration for JSON-formatted logs with extra context."""

import logging
import logging.config
import os


class ExtraContextFilter(logging.Filter):
    """_summary_.

    Args:
        logging (_type_): _description_
    """

    def __init__(self, context: dict | None = None):
        """_summary_ ."""
        super().__init__()
        self.context = context or {}

    def filter(self, record: logging.LogRecord) -> bool:
        """_summary_ ."""
        for k, v in self.context.items():
            if not hasattr(record, k):
                setattr(record, k, v)
        return True


def _logs_dir(default_root: str) -> str:
    """Get the logs directory."""
    # default_root should be repository root
    return os.getenv("LOG_DIR", os.path.join(default_root, "logs"))


def setup_json_logging(
    app_name: str = "testonsave",
    level: str | None = None,
    log_file: str | None = None,
    to_console: bool = True,
) -> None:
    """JSON logging with extra context."""
    # Resolve paths and options
    project_root = os.path.dirname(
        os.path.dirname(__file__)
    )  # repo root (parent of src)
    logs_dir = _logs_dir(project_root)
    os.makedirs(logs_dir, exist_ok=True)

    lvl = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    file_path = log_file or os.getenv(
        "LOG_FILE", os.path.join(logs_dir, f"{app_name}.log")
    )

    # Common context (appears on every log line)
    context = {
        "app": app_name,
        "env": os.getenv("ENV", "dev"),
        "run_id": os.getenv("RUN_ID", None),
    }

    # Build dictConfig so pytest and app share identical config
    handlers = {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": lvl,
            "formatter": "json",
            "filters": ["context"],
            "filename": file_path,
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
        }
    }
    if to_console:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "level": lvl,
            "formatter": "json",
            "filters": ["context"],
            "stream": "ext://sys.stdout",
        }

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "context": {
                    "()": f"{__name__}.ExtraContextFilter",
                    "context": {k: v for k, v in context.items() if v is not None},
                }
            },
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.json.JsonFormatter",
                    # newline-delimited JSON (one event per line)
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s\
                          %(module)s %(funcName)s %(lineno)d \
                        %(process)d %(threadName)s %(app)s %(env)s %(run_id)s",
                    "json_ensure_ascii": False,
                    "json_indent": None,
                    "rename_fields": {
                        "asctime": "timestamp",
                        "levelname": "level",
                        "name": "logger",
                        "funcName": "func",
                        "lineno": "line",
                        "threadName": "thread",
                    },
                }
            },
            "handlers": handlers,
            "root": {"level": lvl, "handlers": list(handlers.keys())},
        }
    )
