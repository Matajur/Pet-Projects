import logging


log_format = 'Time: "%(asctime)s", Level: "%(levelname)s", Module: "%(name)s", Function: "%(funcName)s", Line: "%(lineno)s", Result: "%(message)s"'

file_handler = logging.FileHandler("dump.logs")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(log_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(log_format))


def get_logger_all(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def get_logger_error(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(file_handler)
    return logger


if __name__ == "__main__":
    logger = get_logger_error(__name__)

    def baz(el: str):
        logger.info("Start function baz")
        logger.debug(f"el={el}")

    def foo():
        logger.error("Exception!")

    baz("test")
    foo()
