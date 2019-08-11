import yaml
import unittest
import logging
import getpass
import time
import traceback
import pandas as pd
from sqlalchemy import create_engine
import urllib

import farm.config as CONFIG

class Logger(logging.Handler):
    def __init__(self, config, con, *args, **kwargs):
        super(logging.Handler, self).__init__(*args, **kwargs)
        # yaml config file
        self.config = config
        # sql connection already established
        self.con = con
        self.get_user()

        today = time.strftime("%Y-%m-%d")
        logger_ = logging.getLogger(__name__)
        file_handler = logging.FileHandler('%s/farm_%s.log' % (CONFIG.logs.dir, today))
        formatter = logging.Formatter(
            '%(asctime)s;'
            '%(name)s;'
            '%(levelname)s;'
            '%(funcName)s;'
            '%(message)s',
            datefmt='%Y-%m-%d %I:%M:%S %p'
        )
        file_handler.setFormatter(formatter)
        logger_.addHandler(file_handler)
        logger_.setLevel(logging.INFO)

        self.logger = logging.LoggerAdapter(logger_, self.user)


    def get_traceback(self):
        tb_list = list(traceback.extract_stack(None, 4)[0])
        return tb_list

    def get_function(self):
        function_name = self.get_traceback()[2]
        function_name = {'func_name': function_name}
        return function_name

    def get_module(self):
        module_name = self.get_traceback()[0].split('/')[-1]
        module_name = {'module_name': module_name}
        return module_name

    def get_time(self):
        today = time.strftime("%Y-%m-%d %I:%M:%S")
        today = {'today': today}
        return today

    def get_user(self):
        # add username to logs
        user = getpass.getuser()
        self.user = {'user': user}

    def info(self, message):
        # log message
        level = {'level':'INFO'}
        func_name = self.get_function()
        mod_name = self.get_module()
        today = self.get_time()
        user = self.user
        self.logger.info(message)

    def error(self, message):
        # error message
        level = {'level':'ERROR'}
        func_name = self.get_function()
        mod_name = self.get_module()
        today = self.get_time()
        user = self.user
        self.logger.error(message)

    def exception(self, message):
        # exception message
        level = {'level':'EXCEPTION'}
        func_name = self.get_function()
        mod_name = self.get_module()
        today = self.get_time()
        user = self.user
        self.logger.exception(message)
