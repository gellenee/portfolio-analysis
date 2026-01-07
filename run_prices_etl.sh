#!/bin/bash

# move to proj directory
cd data/etl/jobs.py || exit 1

python jobs.py

echo "ETL run completed at $(date)" >> etl_log.txt


