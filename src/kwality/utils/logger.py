import logging


def get_logger(name: str) -> logging.Logger:
    try:
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    except Exception as exception:
        print(f"Failed to get logger: {exception}")
        raise
