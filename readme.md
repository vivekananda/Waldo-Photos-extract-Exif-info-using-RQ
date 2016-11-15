# Prerequisites
  - redis

# Settings
update settings.py file for all confugurable parameters

# Install
  - virtualenv waldoenv
  - source waldoenv/bin/activate
  - pip install -r requirements.txt
  

# Start workers
Start multiple workers based on the configurations of your system
  - source waldoenv/bin/activate
  - rq  worker --exception-handler startworker.retry_handler  download_queue read_exif_queue store_data_in_db_queue
  - rq  worker --exception-handler startworker.retry_handler  download_queue
  
# Logging
  - tail -f waldophotos.log
  
# Monitoring
Start rq-dashboard and open http://localhost:9181 in browser
  - rq-dashboard
  