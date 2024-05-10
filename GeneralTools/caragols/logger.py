import getpass
import json
import logging.config
import logging.handlers
import sys
from pathlib import Path

LOG_HANDLERS: list[str]
CONFIG_PATH = Path(__file__).parent / 'config-caragols.json'

def load_config():
    global LOG_HANDLERS

    config = json.loads(CONFIG_PATH.read_text())
    logging_config = config['logging']

    log_dir = Path(logging_config['directory']).expanduser().absolute()
    if logging_config['use_user_subdir']:
        log_dir /= getpass.getuser()
    log_dir.mkdir(parents=True, exist_ok=True)
    console_log_level = logging_config['console_log_level']

    root_log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "caragols_basicFormatter": {
                "format": "[%(asctime)s %(levelname)s] - %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "caragols_verboseFormatter": {
                "format":
                    "[%(asctime)s %(levelname)s %(name)s %(filename)s:%(funcName)s:%(lineno)d] - %(message)s",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
            "caragols_jsonFormatter": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
                "format": "%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(filename)s %(module)s %(process)d %(processName)s %(thread)d %(funcName)s %(lineno)d %(message)s"
            }
        },
        "handlers": {
            "caragols_consoleHandler": {
                "level": console_log_level,
                "class": "logging.StreamHandler",
                "formatter": "caragols_basicFormatter",
                "stream": sys.stdout,
            },
            "caragols_plaintextFileHandler": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "caragols_verboseFormatter",
                "filename": log_dir / 'log.txt',
                "maxBytes": 2e6 # 2MB
            },
            "caragols_jsonFileHandler": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "caragols_jsonFormatter",
                "filename": log_dir / 'log.jsonl',
                "maxBytes": 2e6 # 2MB
            },
        },
        "loggers": {
            # when used a library (python api), there should be no handlers configured, so users of the lib can configure logs as they wish
            # when used as an CLI / directly, we will add our specific handlers
            "caragols": {
                "level": "DEBUG",
                "handlers": [],
            },
            # "register" our handlers, but they won't be used by root
            "root": {
                "handlers": ["caragols_consoleHandler", "caragols_plaintextFileHandler", "caragols_jsonFileHandler"]
            }
        },
    }

    LOG_HANDLERS = root_log_config['handlers'].keys()
    return root_log_config


logging.config.dictConfig(config=load_config())
LOGGER = logging.getLogger('caragols')
