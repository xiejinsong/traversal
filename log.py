#!/usr/bin/python
#encoding=utf-8
import logging
import logging.handlers

logger = logging.getLogger("traversal")
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
LOG_FILE = "traversal.log"
fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024)
#fh = logging.FileHandler('traversal.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
