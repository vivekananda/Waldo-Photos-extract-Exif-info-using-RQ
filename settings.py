import logging

DEBUG = False
bucket_url = "http://s3.amazonaws.com/waldo-recruiting/"
download_dir = "data"
db_host = "localhost"
db_port = 6379

download_queue = "download_queue"
read_exif_queue = "read_exif_queue"
store_data_in_db_queue = "store_data_in_db_queue"

max_retry_count = 10


logging.basicConfig(filename='waldophotos.log',level=logging.INFO)
