import logging
import logging.config
import sys

from .env import Environment

__all__ = ["getLogger"]

logging.config.dictConfig({"version": 1, "disable_existing_loggers": True})


class _CustomLogger(logging.getLoggerClass()):
    TRACE: int = logging.DEBUG - 5
    """Trace log level"""

    def trace(self, msg: str, *args, **kwargs):
        """Log 'msg % args' with severity 'TRACE'."""
        if self.isEnabledFor(self.TRACE):
            self._log(self.TRACE, msg, args, **kwargs)


logging.addLevelName(_CustomLogger.TRACE, "TRACE")


def getLogger(name: str):
    # logger = logging.getLogger(name)
    logger = _CustomLogger(name)
    logger.setLevel(Environment().LOG_LEVEL)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter(
        "[%(levelname)s] %(pathname)s:%(lineno)d | %(message)s"
    )
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger
