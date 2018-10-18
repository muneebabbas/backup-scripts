#!/usr/bin/env python3
"""This script will run an rsync backup to backup-server-1 and a mounted hard drive
It will then make a post request to a webhook about whether the backup was successful or not
"""

import subprocess
import logging
from logging.handlers import RotatingFileHandler
import time
import requests
import os

BACKUP_DIR = '/home/muneebabbas/work/backup-scripts'
LOG_FILE_SIZE = 5*1024*1024 # 5MB
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
WEBHOOK_URL = 'http://192.168.1.102:9912/webhooks/script'
TIME = None

# Change working directory
os.chdir(BACKUP_DIR)

scripts = [
    {
        'path': 'scripts/backup-server.sh',
        'description': 'Full system backup to backup-server-1 (HP laptop)',
        'logfile': 'logs/backup-server.log'
    },
    {
        'path': 'scripts/wd-1.sh',
        'description': 'Full system backup to WD-1 attached hard drive',
        'logfile': 'logs/wd-1.log'
    }
]

# The lines of logs which contain these will be ignored
FILTERS = ['skipping non-regular file', 'var/lib/docker']

def clean_rsync_logs(logs):
    """Use the FILTERS array to exclude lines"""
    logs_array = logs.split('\n')
    logs_array = filter(
        lambda x: not any(map(lambda y: y in x, FILTERS)),
        logs_array
    )
    return "\n".join(list(logs_array))

def get_script_logger(script):
    """Get logger for the particular script"""
    logger = logging.getLogger(script['path'])
    handler = RotatingFileHandler(script['logfile'], maxBytes=LOG_FILE_SIZE)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def timeit(method):
    def timed(*args, **kw):
        global TIME
        ts = time.time()
        result = method(*args, **kw)
        TIME = time.time() - ts
        return result
    return timed

@timeit
def run_script(path_to_script):
    """Run the script and return the returncode, stdout and stderr"""
    result = subprocess.run(path_to_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode, result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

def main():
    # Backup to backup-server and attached hard drive
    for script in scripts:
        returncode, stdout, stderr = run_script(script['path'])
        stdout = clean_rsync_logs(stdout)
        logger = get_script_logger(script)
        logger.info(
            '%s\n%s\n%s\n%s',
            'Path: {0}'.format(script['path']),
            'Description: {0}'.format(['description']),
            'STDERR: {0}'.format(stderr),
            'STDOUT: {0}'.format(stdout)
        )
        try:
            requests.post(WEBHOOK_URL, json={
                'path': script['path'],
                'description': script['description'],
                'logfile': script['logfile'],
                'time': round(TIME),
                'returncode': returncode,
                'stderr': stderr,
                'stdout': stdout,
                'type': 'backup'
            })
        except Exception as e:
            logger.exception(e)
            continue

if __name__ == '__main__':
    main()
