import os
import getpass
import glob
from datetime import datetime, timedelta, date
import logging
import time
from sqlalchemy import create_engine

import farm.config as CONFIG

def get_user():
    # add username to logs
    user = getpass.getuser()
    extra = {'user': user}
    return extra

def remove_log(log_file, logger): # pragma: no cover
    os.remove('%s/%s' % (CONFIG.logs.dir, log_file))
    logger.info('Removed %s based on range criteria in config yaml file.' % log_file)

def month_to_quarter(month):
    return month // 4 + 1

def parse_date(log_file):
    log_file = log_file.split('.')[0]
    log_date = log_file.split('_')[-1]
    year, month, day = map(int, log_date.split('-'))
    quarter = month_to_quarter(month)
    _, week, _ = datetime(year, month, day).date().isocalendar()

    return day, week, quarter


def clean_logs(report_config, logger):
    '''
    Remove logs from local storage after certain period of time.

    Parameters
    ----------
    report_config: dict
        contains info on how long logs can exist before removing them
    logger: object
        writes info to file
    '''
    today = datetime.now()
    _, week, _ = date.isocalendar(today)
    day, month, quarter = today.day, today.month, month_to_quarter(today.month)

    os.chdir(CONFIG.logs.dir)
    log_files = glob.glob('*.log')

    for log_file in log_files:
        log_day, log_week, log_quarter = parse_date(log_file)
        if report_config['keep_logs_for'] == 'd':
            if day != log_day: # pragma: no cover
                remove_log(log_file, logger)
        elif report_config['keep_logs_for'] == 'q':
            if quarter != log_quarter: # pragma: no cover
                remove_log(log_file, logger)
        elif report_config['keep_logs_for'] == 'w':
            if week != log_week: # pragma: no cover
                remove_log(log_file, logger)
        else:
            logger.info('Not a possible log period to remove for')
            return -1
        return 0
