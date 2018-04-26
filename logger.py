import logging


class Logger:
    def __init__(self):
        self.err_logger = logging.getLogger('errors')
        self.act_logger = logging.getLogger('actions')

    def errors(self):
        self.err_logger.setLevel(logging.WARNING)
        self.file_handler('main_log.log')
        self.err_logger.addHandler(self.file_handler)

    def actions(self):
        self.act_logger.setLevel(logging.INFO)
        self.file_handler('actions.log')
        self.act_logger.addHandler(self.file_handler)

    def formatter(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(format)

    def file_handler(self, arg):
        self.formatter()
        self.file_handler = logging.FileHandler(arg, encoding='utf-8')
        self.file_handler.setFormatter(self.formatter)

    def errors_log(self, arg):
        if not self.err_logger.hasHandlers():
            self.errors()
        self.err_logger.warning(arg)

    def actions_log(self, arg):
        if not self.act_logger.hasHandlers():
            self.actions()
        self.act_logger.info(arg)
