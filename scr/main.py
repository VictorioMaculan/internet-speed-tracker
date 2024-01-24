from datetime import datetime
from sqlite3 import connect
from time import sleep
import speedtest as spt
import pandas as pd
import numpy as np
import logging
import argparse
import schedule

frmt = '[%(levelname)s : %(created)f] - %(message)s'
logging.basicConfig(format=frmt, level=logging.INFO)

builtin_tester = spt.Speedtest()


def run_speedtest(tester=builtin_tester) -> dict:
    '''Run a speedtest.'''
    tester.download()
    tester.upload()
    return tester.results.dict()


def _main(file, cache={'run': 0}):
    result = run_speedtest()
    
    server = pd.DataFrame(result.pop('server'), index=[cache['run']])
    client = pd.DataFrame(result.pop('client'), index=[cache['run']])
    data = pd.DataFrame(result, index=[cache['run']])
    
    tables = {'server_data': server,
              'client_data': client,
              'main_data': data}
    with connect(file) as con:
        for key, item in tables.items():
            item.to_sql(name=key, con=con, if_exists='append')
            
    cache['run'] += 1
    logging.info('A speedtest was run and registered successfully.')
    
    
offsets = {'w': 'weeks', 
           'd': 'days', 
           'h': 'hours', 
           'm': 'minutes'}

parser = argparse.ArgumentParser(prog='trackyournet')
parser.add_argument('interval')
parser.add_argument('unit', choices=offsets.keys())
parser.add_argument('file')

args = parser.parse_args()

scheduler = schedule.Scheduler()
job = schedule.Job(interval=int(args.interval), scheduler=scheduler)
job.unit = offsets[args.unit]
job.do(_main, file=args.file)


while True:
    scheduler.run_pending()
    