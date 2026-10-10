import logging
import uuid

from kwality.utils.logger import get_logger


def test_get_logger_returns_logger_with_stream_handler():
    """
    Test that get_logger returns a logger with a StreamHandler attached.
    """
    logger_name = f"kwality.test_logger.{uuid.uuid4().hex}"
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)
    logger.propagate = False

    result = get_logger(logger_name)

    assert isinstance(result, logging.Logger)
    assert result.name == logger_name
    assert result.level == logging.INFO
    assert len(result.handlers) == 1
    assert isinstance(result.handlers[0], logging.StreamHandler)


def test_get_logger_does_not_add_duplicate_handlers():
    """
    Test that get_logger does not add duplicate handlers when 
    called multiple times with the same logger name.
    """
    logger_name = f"kwality.test_logger_duplicate.{uuid.uuid4().hex}"
    logger = logging.getLogger(logger_name)
    logger.handlers.clear()
    logger.setLevel(logging.NOTSET)
    logger.propagate = False

    result = get_logger(logger_name)
    original_handler_count = len(result.handlers)
    same_logger = get_logger(logger_name)

    assert same_logger is result
    assert len(same_logger.handlers) == original_handler_count
