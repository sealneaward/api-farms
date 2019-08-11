import os
import getpass
import glob
from datetime import datetime, timedelta, date
import logging
import time
from sqlalchemy import create_engine

# python2 and python3 compatible
try:
    from urllib.parse import quote_plus
except ImportError:
     from urllib import pathname2url as quote_plus

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

def connection(report_config):
    connection_str = (r'DRIVER=%s;SERVER=%s;DATABASE=%s;Trusted_Connection=%s;' % (
        report_config['driver'],
        report_config['server'],
        report_config['database'],
        report_config['trusted_connection']
    ))
    aml_internal_params = quote_plus(connection_str)
    con = create_engine('mssql+pyodbc:///?odbc_connect=%s' % aml_internal_params)
    return con

def check_credentials(report_config):
    '''
    Check the credentials file to see if the file was modified on the date of execution.
    If it was not modified, return False.

    Parameters
    ----------
    report_config: dict
        report configuration information

    Returns
    -------
    modified: bool
        indicator of whether credentials were updated or not
    '''

    file_modified_time = os.path.getmtime(report_config['credentials'])
    file_modified_time = datetime.utcfromtimestamp(file_modified_time).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')
    if file_modified_time != today:
        return False
    else:
        return True


# Outputs to MIS_Internal table
def create_sql_output(df, output_table, report_config, logger):
    try:
        df.to_sql(name=output_table,
                  schema='db_datareader',
                  if_exists='replace',
                  index=False,
                  con=connection(report_config)
                 )
    except Exception as e:
        logger.exception('Error: failed to write data to sql.' + str(e))
        print('Error: failed to write data to sql.' + str(e))
