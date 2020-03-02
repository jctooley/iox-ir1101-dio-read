#!/usr/bin/env python

# Made for Python 2.

import os
import sys
import time
import serial
import logging
import serial.tools.list_ports

if __name__ == "__main__":

    # Location of the directory to store log file, otherwise use /tmp
    log_file_dir = os.getenv("CAF_APP_LOG_DIR", "/tmp")
    log_file_path = os.path.join(log_file_dir, "iox-serial.log")

    # set up logging to file 
    logging.basicConfig( 
        filename=log_file_path,
        level=logging.INFO, 
        format='[%(asctime)s]{%(pathname)s:%(lineno)d}%(levelname)s- %(message)s', 
        datefmt='%H:%M:%S'
    ) 

    # set up logging to console 
    console = logging.StreamHandler() 
    console.setLevel(logging.DEBUG) 

    # set a format which is simpler for console use 
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter) 

    # add the handler to the root logger 
    logging.getLogger('').addHandler(console) 
    logger = logging.getLogger(__name__)

    logger.info('Starting application...')

    ports = serial.tools.list_ports.comports()
    logger.info('Ports available:\n')
    
    iter = 1000;
    while (iter > 0):
        logger.info(">> Iteration:" + str(iter) + " <<")
        for port, desc, hwid in sorted(ports):
            portx = "+  {}: {} [{}]".format(port, desc, hwid)
            logger.info(portx)

            try:
                ser = serial.Serial(port)  # open serial port
                if (ser.inWaiting()>0):
                    line = ser.readline() 
                    logger.info('data: ' + line)         # check which port was really used
                else:
                    logger.info("no data on serial line")
            except:
                logger.info("Unexpected error:" + str(sys.exc_info()[1]))
        iter = iter-1
        if (iter>0):
            time.sleep(2)
                    
    ser.close()             # close port

    logger.info("All done. Goodbye!\n")
