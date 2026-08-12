import logging
import sys

from pythonjsonlogger import jsonlogger


class TasklyJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not hasattr(record, "request_id"):
            log_record["request_id"] = None


def configure_logging():
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = TasklyJsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s"
    )

    handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(handler)