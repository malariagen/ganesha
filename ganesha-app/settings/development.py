from common import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG

import sqlparse
import logging

class sqlformatter(logging.Formatter):
    def format(self, record):
        if record.sql:
            return sqlparse.format(record.sql, reindent=True, keyword_case="upper")

API_LIMIT_PER_PAGE = 0

LOGGING = {
    'version'       : 1,
    'formatters': {
        'sqlformatter': {
            '()': sqlformatter
        },
        },
    'handlers': {
        'console_sql': {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter'     : 'sqlformatter',
            },
        },
    'loggers': {
        # Only becomes active with DEBUG = True
        'django.db.backends': {
            'level'         : 'DEBUG',
            'handlers'      : ['console_sql'],
            },
        },
    }