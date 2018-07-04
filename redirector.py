#!/usr/bin/python
import sys
import json
import logging
import hashlib
import time
from urlparse import urlparse,urlsplit,parse_qs



def modify_url(line, config):
    try:
        old_url = line.split(' ')[0]
#        old_ip  = line.split(' ')[1]

        logging.info('Receiving requete old url : '+old_url)
        parsed = urlparse(old_url)
        path = parsed.path
        param_t = parse_qs(parsed.query)['t'][0]
        param_k = parse_qs(parsed.query)['k'][0]
        logging.info(config["key"]+param_t+path)
        k = hashlib.md5(config["key"]+'&'+param_t+'&'+path).hexdigest()[12:-12]
#        k = hashlib.md5(config["key"]+param_t+path).hexdigest()[12:-12]
        logging.info("k caculated is :"+k)
    except Exception, e:
        logging.error(line + str(e))
        return "403:"+line

    try:
        if int(param_t) + int(config['valid_time']) < int(time.time()) :
            raise Exception("url expires")
        elif k != param_k :
            raise Exception(k + " k caculated is not match with "+ param_k)
        else :
            logging.info("test ok!")

    except Exception, e:
        logging.error(line + str(e))
        return "403:"+line
        
    return line


def main():
    levels = (logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR, logging.CRITICAL)

#    LOGLEVEL = logging.WARNING
    LOGLEVEL = logging.INFO

    LOG_FILENAME = '/tmp/squid-redirector.log'
    logging.basicConfig(filename=LOG_FILENAME,level=LOGLEVEL,format='%(asctime)s %(levelname)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S')


    logging.info('---------------------------------------')
    logging.info('squid-redirector.py')
    logging.info('---------------------------------------')
    config_file = sys.argv[1]
    with open(config_file) as f:
        config = json.load(f)
        config_keys = config.keys()

    for key in config_keys:
        logging.info("get key"+key+"get value"+config[key])

    while True:
        line = sys.stdin.readline()
        logging.info('Receiving requete : '+line)
        new_line = modify_url(line, config)
        sys.stdout.write(new_line)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
