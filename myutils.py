import urllib2
import urlparse
import logging

import exifread
import os
from redis import Redis
from rq import Queue
from settings import *


def _getqueue(queue_name):
    """get Queue instance with given name"""
    redis_conn = _getrediscon()
    return Queue(queue_name, connection=redis_conn)


def _getfilepath(key):
    return os.path.join(download_dir, key)


def _getrediscon():
    return Redis(host=db_host, port=db_port, db=0)


def download_image(key):
    """Download the image identified by the key and store it in local dir"""
    image_url = urlparse.urljoin(bucket_url, key)
    file_path = _getfilepath(key)

    if not (DEBUG and os.path.exists(file_path)):
        logging.info("image download started" + key)
        response = urllib2.urlopen(image_url)
        CHUNK = 1024
        with open(file_path, 'wb') as f:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)

        logging.info("image download finished" + key)

        f.close()
    q = _getqueue(read_exif_queue)
    q.enqueue(extract_exif_info, key)

    return file_path


def extract_exif_info(key):
    """Extract Exif info from the downloaded file"""
    logging.info("extracing tags :: " + key)
    file_path = os.path.join(download_dir, key)
    f = open(file_path, 'rb')
    tags = exifread.process_file(f)
    logging.info("extraced tags :: " + key)
    q = _getqueue(store_data_in_db_queue)

    q.enqueue(store_tags_in_db, key, tags)

    return tags


def store_tags_in_db(key, tags):
    """save Exif tags in db """
    logging.info("storing tags in db :: " + key)
    redis_conn = _getrediscon()
    if tags:
        redis_conn.hmset(key, tags)
    # if DEBUG:
    #     print(redis_conn.hgetall(key))
    logging.info("store tags in db complete :: " + key)


def cleanup_image(key):
    file_path = _getfilepath(key)
    if not DEBUG and os.path.exists(file_path):
        os.remove(file_path)
