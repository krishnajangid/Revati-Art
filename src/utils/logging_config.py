import json
import logging
import os
import time

from utils.config import settings


class CustomLogFilter(logging.Filter):
    user_email = None
    request_id = None
    request_ip_addr = None

    def filter(self, record):
        record.email = CustomLogFilter.user_email or None
        record.request_id = CustomLogFilter.request_id or f'fs_req_{int(time.time() * 1000)}'

        return True


class JSONFormatter(logging.Formatter):
    def format(self, record):
        default_keys = ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 'module',
                        'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName', 'created', 'msecs',
                        'relativeCreated', 'thread', 'threadName', 'processName', 'process', 'email',
                        'request_ip_addr', 'request_id']
        extra = {}
        for key in record.__dict__:
            if key not in default_keys:
                extra[key] = record.__dict__[key]

        log_data = {
            'timestamp': self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            'level': record.levelname,
            'message': record.getMessage(),
            'pathname': f"{record.pathname}:{record.lineno}",
            'function': record.funcName,
            'email': record.email if hasattr(record, 'email') else None,
            'request_id': record.request_id if hasattr(record, 'request_id') else None,
            'request_ip_addr': record.request_ip_addr if hasattr(record, 'request_ip_addr') else None,
        }
        log_data.update(extra)
        if record.exc_text:
            log_data["traceback"] = record.exc_text
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_data, default=str)


def get_formatter(*args, **kwargs):
    if settings.DEPLOYMENT_TYPE in ("local", "dev"):
        return logging.Formatter(
            settings.LOG_FORMAT,
            datefmt=settings.LOG_DATE_FMT
        )
    return JSONFormatter()


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            '()': get_formatter,
        },
    },
    'filters': {
        'customLogFilter': {
            '()': CustomLogFilter,
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['customLogFilter']
        },
        "access": {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['customLogFilter']
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        "boto3": {
            'level': 'WARNING',
            'propagate': False
        },
        "botocore": {
            'level': 'WARNING',
            'propagate': False
        },
        "s3transfer": {
            'level': 'WARNING',
            'propagate': False
        },
        "urllib3": {
            'level': 'WARNING',
            'propagate': False
        },
        "multipart": {
            'level': 'WARNING',
            'propagate': False
        },
        "uvicorn": {
            "handlers": ["access"],
            "level": "DEBUG",
            "propagate": True
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False
        },
        'uvicorn.error': {
            'level': 'INFO',
            'propagate': False
        }
    }
}
