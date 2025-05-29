import logging


def configure_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=logging.INFO, format=log_format, force=True)

    loggers_to_configure = ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]

    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False


configure_logging()

logger = logging.getLogger("gpt4o-mini-logger")
