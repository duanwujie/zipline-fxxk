#!/bin/bash

zipline run --bundle my-db-bundle -f example/buy_and_hold.py --start 2016-1-1 --end 2018-1-1 -o dma.pickle

