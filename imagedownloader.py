import urllib2
import logging

import xmltodict
from myutils import _getqueue, download_image
from settings import *


def initiate_download():
    """This function is responsible for getting the list of images and setting them in queue for download"""
    if DEBUG:
        xml = open("/Users/vivek/Desktop/waldo-recruiting.xml").read()
    else:
        response = urllib2.urlopen(bucket_url)
        xml = response.read()

    doc = xmltodict.parse(xml)
    for item in doc['ListBucketResult']['Contents']:
        key = item['Key']
        # print key
        q = _getqueue(download_queue)
        q.enqueue(download_image, key)
        # add items to queue


#initiate_download()

if __name__ == "__main__":
    initiate_download()
    # key = "0015A5C3-D186-471F-A032-9E952CFF3CC6.8fedf4e8-8695-4d6d-ad1e-b686daa713a1.jpg"
    # key = "01891213-d911-4562-9947-8548dac09119.undefined.jpg"
    # download_image(key)
    # tags = extract_exif_info(key)
    # store_tags_in_db(key, tags)
    # print(tags)
