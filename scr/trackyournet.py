from os.path import isdir, join
from datetime import datetime
from sqlite3 import connect, OperationalError
import speedtest as spt
import pandas as pd
import logging
import argparse
import schedule
import sys

# * Tester
try:
    builtin_tester = spt.Speedtest()
except Exception:
    logging.error('Check your internet connection.')
    sys.exit()

frmt = '[%(levelname)s : %(asctime)s] - %(message)s'
logging.basicConfig(format=frmt, level=logging.INFO)

offsets = {'week': 'weeks', 
        'day': 'days', 
        'hour': 'hours', 
        'min': 'minutes'}


class StopTYN(BaseException):
    pass


def run_speedtest(tester: spt.Speedtest) -> dict:
    '''Run a simple speedtest.'''
    tester.download()
    tester.upload()
    tester.results.share()
    return tester.results.dict()


def _job_func(file, 
          repeat=None, 
          _cache={'rpt_count': 0}):
    try:
        
        logging.info('A speedtest is being run, do not stop the application.')
        result = run_speedtest(builtin_tester)
        
        idx = [datetime.now()]
        server = pd.DataFrame(result.pop('server'), index=idx)
        client = pd.DataFrame(result.pop('client'), index=idx)
        data = pd.DataFrame(result, index=idx)
        
        data.drop('timestamp', axis=1, inplace=True)
        
        tables = {'server_data': server,
                'client_data': client,
                'main_data': data}
        
        with connect(file) as con:
            for key, item in tables.items():
                item.to_sql(name=key, con=con, if_exists='append')
                
        # --repeat
        _cache['rpt_count'] += 1
        if (repeat is not None) and (_cache['rpt_count'] == repeat):
            raise StopTYN
        
        logging.info('A speedtest was run and registered successfully. ' +
                     '(Run #{})'.format(_cache['rpt_count']))
           
    except (pd.errors.DatabaseError, OperationalError):
        logging.critical('DATABASE ERROR.')
        raise StopTYN

        
def _get_parser():
    parser = argparse.ArgumentParser(prog='trackyournet',
                    description='Tracks your internet speed.')

    parser.add_argument('interval', 
                        type=int,
                        help='The interval between speedtests.')
    parser.add_argument('-u', '--unit', 
                        choices=offsets.keys(), 
                        required=True,
                        help='The unit of `interval`: ' + 
                        'week, day, hour or min (minute)')
    parser.add_argument('-f', '--file', 
                        required=True,
                        help='A path pointing to a sqlite ' + 
                        'database or a directory where the data will ' + 
                        'be allocated (The database will be created if ' + 
                        'it doesn\'t exist).')
    parser.add_argument('-r', '--repeat',
                        type=int,
                        help='How many speedtests will be run ' +
                        'before exiting.')
    
    return parser


def _get_clean_args():
    parser = _get_parser()
    args = parser.parse_args()
    
    args.interval = abs(args.interval)
    args.unit = args.unit.lower()
    if isdir(args.file):
        args.file = join(args.file, 'trackyournet.db')
    
    if args.unit == 'min' and args.interval < 5:
        logging.error('Not too fast, partner! ' + 
                      '(Interval should be at least 5 minutes).')
        sys.exit()
        
    return args
    
    
def command_line_runner():
    args = _get_clean_args()
    
    # * Scheduler
    rep = abs(args.repeat) if args.repeat is not None else None

    scheduler = schedule.Scheduler()
    job = schedule.Job(interval=args.interval, 
                    scheduler=scheduler)
    job.unit = offsets[args.unit]
    job.do(_job_func, file=args.file, repeat=rep)

    # * Runner
    logging.info('Trackyournet started.')
    while True:
        try:
            scheduler.run_pending()
        except (StopTYN, KeyboardInterrupt):
            logging.info('Trackyournet stopped.')
            return


if __name__ == '__main__':
    command_line_runner()
