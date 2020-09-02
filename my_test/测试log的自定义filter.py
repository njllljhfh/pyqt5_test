# -*- coding:utf-8 -*-
import datetime
import json
import logging
import sys
import uuid

print(sys.path)

from log_config.settings import OperationType

logger = logging.getLogger(__name__)

# a = 0
# for i in range(5):
#     timestamp = datetime.datetime.now()
#     print(timestamp)
#     print(timestamp.timestamp())
#     a = timestamp.timestamp()
#
# print("- " * 30)
# print(datetime.datetime.utcfromtimestamp(a) + datetime.timedelta(hours=8))
#
# print("- " * 30)
# print(uuid.uuid4())
# print(uuid.uuid4())
# print(uuid.uuid4())

timestamp = datetime.datetime.now()
t = timestamp.strftime('%Y%m%d%H%M%S%f')
# print(t)

log_type = "debug"
row_key = log_type + "-" + t + "-" + "561d93a8-02ce-40b8-80e4-d7faf7f06c5b"
# print("row_key = {}".format(row_key))
# logger.info("len(row_key) = {}".format(len(row_key)), extra=OperationType.run)
# logger.info("len(row_key) = {}".format(len(row_key)), extra=OperationType.walk)
# logger.info("len(row_key) = {}".format(len(row_key)), extra=OperationType.fly)

logger.info("len(row_key) = {}".format(len(row_key)))
a = {'a': 1}
logger.info(json.dumps(a), extra=OperationType.run)
