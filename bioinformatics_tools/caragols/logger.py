import getpass
import json
import logging.config
import logging.handlers
import sys
from pathlib import Path

LOG_HANDLERS: list[str]
CONFIG_PATH = Path(__file__).parent / 'logging-config.json'

def load_config():
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
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
            "caragols_basicFormatter": {
                "format": "[%(asctime)s %(levelname)s] - %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "caragols_verboseFormatter": {
                "format":
                    "[%(asctime)s %(levelname)s %(process)d %(name)s %(filename)s:%(funcName)s:%(lineno)d] - %(message)s",
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
                "maxBytes": 2e6, # 2MB
                "backupCount": 100,
            },
            "caragols_jsonFileHandler": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "caragols_jsonFormatter",
                "filename": log_dir / 'log.jsonl',
                "maxBytes": 2e6, # 2MB
                "backupCount": 100,
            },
        },
        "loggers": {
            # when used a library (python api), there should be no handlers configured, so users of the lib can configure logs as they wish
            # when used as an CLI / directly, we will add our specific handlers
            "caragols": {
                "level": "DEBUG",
                "handlers": [],
            },
        },
    }

    return root_log_config



def config_logging_for_app():
    """(re)Configure the main logger for running as a CLI app

    We default to running in a "library" logging config, meaning no handlers are added to the logger, so clients can add
    their own, as recommended by https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library

    This allows us to still leverage the convenience of dictConfig
    """
    global LOGGER
    log_config = load_config()
    log_handlers = log_config['handlers'].keys()
    log_config['loggers']['caragols']['handlers'] = log_handlers
    logging.config.dictConfig(config=log_config)
    LOGGER = logging.getLogger('caragols')

logging.config.dictConfig(config=load_config())
LOGGER = logging.getLogger('caragols')
