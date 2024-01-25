from datetime import datetime
from sqlite3 import connect
import speedtest as spt
import pandas as pd
import logging
import argparse
import schedule
import sys


frmt = '[%(levelname)s : %(asctime)s] - %(message)s'
logging.basicConfig(format=frmt, level=logging.INFO)


# * Tester
try:
    builtin_tester = spt.Speedtest()
except Exception:
    logging.error('Check your internet connection.')
    sys.exit()


class StopTYS(BaseException):
    pass


def run_speedtest(tester=builtin_tester) -> dict:
    '''Run a simple speedtest.'''
    tester.download()
    tester.upload()
    tester.results.share()
    return tester.results.dict()



def _main(file):
    try:
        
        result = run_speedtest()
        
        idx = [datetime.now()]
        server = pd.DataFrame(result.pop('server'), index=idx)
        client = pd.DataFrame(result.pop('client'), index=idx)
        data = pd.DataFrame(result, index=idx)
        
        tables = {'server_data': server,
                'client_data': client,
                'main_data': data}
        
        with connect(file) as con:
            for key, item in tables.items():
                item.to_sql(name=key, con=con, if_exists='append')
                
        logging.info('A speedtest was run and registered successfully.')
        
        # --repeat
        global rep
        if rep is not None:
            rep -= 1
            if not rep:
                raise StopTYS
            
    except pd.errors.DatabaseError:
        logging.critical('DATABASE ERROR.')
        raise StopTYS

        

# * Avaiable offsets
offsets = {'week': 'weeks', 
           'day': 'days', 
           'hour': 'hours', 
           'min': 'minutes'}


# * Terminal parser
parser = argparse.ArgumentParser(prog='trackyournet')
parser.add_argument('interval')
parser.add_argument('-u', '--unit', choices=offsets.keys(), 
                    required=True)
parser.add_argument('-f', '--file', required=True)
parser.add_argument('-r', '--repeat')
args = parser.parse_args()


# * Scheduler
scheduler = schedule.Scheduler()
job = schedule.Job(interval=int(args.interval), 
                   scheduler=scheduler)
job.unit = offsets[args.unit]
job.do(_main, file=args.file)


# * Main
logging.info('Trackyournet started.')
rep = abs(int(args.repeat)) if args.repeat is not None else None
while True:
    try:
        scheduler.run_pending()
    except (StopTYS, KeyboardInterrupt):
        logging.info('Trackyournet stopped.')
        sys.exit()
    