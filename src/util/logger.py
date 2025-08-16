import logging
from logging import LogRecord
from typing import Any

from core.contextvar.trace_id import trace_id_ctx


class TraceIdFilter(logging.Filter):
    def filter(self, record: LogRecord):
        record.trace_id = trace_id_ctx.get()
        return True


def logger_config() -> dict[str, Any]:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "trace_id": {
                "()": TraceIdFilter,  # 呼叫我們的 Filter class
            }
        },
        "formatters": {
            "default": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s [trace_id=%(trace_id)s] %(levelname)s: %(message)s",
            },
            "json": {
                "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "trace_id": "%(trace_id)s", "message": "%(message)s"}',
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "filters": ["trace_id"],
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
