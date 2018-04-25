import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger('bot')
        self.logger.setLevel(logging.INFO)
        self.formatter()

    def formatter(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(format)

    def file_handler(self):
        file_handler = logging.FileHandler('main_log.log', encoding='utf-8')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def connection_logs(self, arg):
        self.file_handler()
        self.logger.warning(arg)

