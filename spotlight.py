import os
import shutil
import json
import time
import logging
from pathlib import Path


# create logger
logging.basicConfig(filename='logs.log',level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p')
logger = logging.getLogger("spotlight")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class Spotlight:
  TIMEOUT = 60
  MIN_SIZE = 200000
  HOME = os.path.expanduser("~")

  DIR_DESTINATION = "Pictures\\spotlight"
  DIR_SOURCE = "AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"

  def __init__(self):
    self.DIR_DESTINATION = os.path.join(self.HOME, self.DIR_DESTINATION)
    self.DIR_SOURCE = os.path.join(self.HOME, self.DIR_SOURCE)

  def start(self, timeout=None, min_size=None):
    self.TIMEOUT = timeout if timeout is not None else self.TIMEOUT
    self.MIN_SIZE = min_size if min_size is not None else self.MIN_SIZE

    logger.info("Service Started; {} Sec Timeout; {}kb Min file size".format(self.TIMEOUT, self.MIN_SIZE/1000))

    # Create spotlight directory if it doesn't exist
    if not os.path.isdir(self.DIR_DESTINATION):
      logger.warning("Spotlight directory does not exist")
      logger.info("Creating spotlight directory")
      os.mkdir(self.DIR_DESTINATION)
      if os.path.isdir(self.DIR_DESTINATION):
        logger.info(self.DIR_DESTINATION)
      else:
        logger.warning("Failed to create directory")

    # Fetch images while the program is running    
    try:
      while True:
        for filename in os.listdir(self.DIR_SOURCE):
          new_filename = os.path.join(self.DIR_DESTINATION, filename+".jpg")
          old_filename = os.path.join(self.DIR_SOURCE, filename)
          filesize = os.path.getsize(old_filename)
          
          # copy files that are up to MIN_SIZE 
          if filesize >= self.MIN_SIZE and not os.path.isfile(new_filename):
            shutil.copyfile(old_filename, new_filename, follow_symlinks=True)
            logger.info("{} - {}kb".format(filename, filesize/1000))

        time.sleep(self.TIMEOUT)
    except KeyboardInterrupt:
      logger.critical("Keyboard Interrupt Detected: Exiting")
      exit(1)

spotlight = Spotlight()
spotlight.start(60, 100000)
