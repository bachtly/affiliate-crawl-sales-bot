import logging
import logging.handlers

import logging_loki

from utils.decorator.Singleton import singleton

LOKI_URL = "http://172.17.0.1:3100/loki/api/v1/push"


@singleton
class Logger:
    def __init__(self, applicationName):
        self.applicationName = applicationName

    def Setup(self):
        handler = logging_loki.LokiHandler(
            # Queue(-1),
            url=LOKI_URL,
            tags={"application": self.applicationName},
            auth=("username", "password"),
            version="1",
        )

        formatter = logging.Formatter(
            f'[%(levelname)s] %(pathname)s: %(funcName)s():%(lineno)d \n%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler('log/info.log')
        fileHandler.setFormatter(formatter)

        logger = logging.getLogger("my-logger")
        logger.addHandler(handler)
        logger.addHandler(fileHandler)
        logger.setLevel(logging.INFO)

        return logger

    def Info(self, message, data=None):
        logger = self.Setup()
        message = self.FillMessageWithData(message, data)
        logger.info(message)

    def Warn(self, message, data=None):
        logger = self.Setup()
        message = self.FillMessageWithData(message, data)
        logger.warning(message, stack_info=True)

    def Error(self, message, data=None):
        logger = self.Setup()
        message = self.FillMessageWithData(message, data)
        logger.error(message, stack_info=True, exc_info=True)

    def FillMessageWithData(self, message, data):
        message += '\n'

        if data is None: return message

        message += '{\n'
        for (key, val) in data.items():
            message += '\t'
            message += f'{key}: {val}'
            message += '\n'
        message += '}\n'

        return message
