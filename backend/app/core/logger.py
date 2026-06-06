import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("/tmp/omnis_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def setup_logging(level: str = "INFO"):
    """Configure root logger for the application."""
    root = logging.getLogger()
    if root.handlers:
        # Avoid configuring multiple times in reload scenarios
        return

    level_val = getattr(logging, level.upper(), logging.INFO)
    root.setLevel(level_val)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)
    root.addHandler(stream_handler)

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)

def get_logger(name: str):
    return logging.getLogger(name)
