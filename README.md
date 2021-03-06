# Waldo-Photos-extract-Exif-info-using-RQ
Working with Redis Queues: Queueing jobs and processing them in the background with concurrent workers

## Problem statement
Using any language and data-store of your choice, write an application that reads a set of photos from a network store (S3), parses the EXIF data from the photos and indexes the EXIF key/value pairs into a query-able store by unique photo.

## Prerequisites
  - redis

## Settings
update settings.py file for all confugurable parameters

## Install
  - virtualenv waldoenv
  - source waldoenv/bin/activate
  - pip install -r requirements.txt
  

## Start workers
Start multiple workers based on the configurations of your system
  - source waldoenv/bin/activate
  - rq  worker --exception-handler exceptionhandler.retry_handler  download_queue read_exif_queue store_data_in_db_queue
  - rq  worker --exception-handler exceptionhandler.retry_handler  download_queue

## Start the process
  - source waldoenv/bin/activate
  - python imagedownloader.py
  
## Logging
  - tail -f waldophotos.log
  
## Monitoring
Start rq-dashboard and open http://localhost:9181 in browser
  - rq-dashboard
 
## Resources
  - S3 Bucket (input): http://s3.amazonaws.com/waldo-recruiting
  - RQ (Redis Queue) http://python-rq.org/

## Scope for improvement
  - As the Exif info is present in header, no need to download complete image
  - Improved downloading of image by continuing from the previous fail point 