#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import datetime
import logging


def creepy_job(m):
    while True:
        os.system("/opt/creeperpy/creeper.sh >> /opt/creeperpy/logs/`date -d today +%Y%m%d`.log 2>&1")
        time.sleep(m * 60)

if __name__ == "__main__":
    creepy_job(30)
