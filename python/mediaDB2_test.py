"""
Test script for assetDB.
"""
import sys
import time

from sqlalchemy import create_engine

import mediaDB2.config as config
import mediaDB2.setup as setup
import mediaDB2.models.modelbase as base
import mediaDB2.utils
from mediaDB2.models import *


def main():
    # print 'args', sys.argv
    reset_tables = False
    if len(sys.argv) > 1:
        if str(sys.argv[1]).lower() == 'false':
            reset_tables = False
        elif str(sys.argv[1]).lower() == 'true':
            reset_tables = True
        else:
            reset_tables = bool(int(sys.argv[1]))

    url = setup.get_database_url()
    engine = create_engine(url, echo=setup.ECHO)

    # Reset Tables
    if reset_tables is True:
        print 'Resetting Tables...'
        base.dropTables(engine)
        base.createTables(engine)

    session = setup.get_session()

    # Find Media
    includes = config.getIncludePaths()
    excludes = config.getExcludePaths()
    for path in includes:
        print 'Find Media...', path
        s = time.time()

        num = mediaDB2.utils.findMedia(session, path, exclude_paths=excludes)

        e = time.time()
        total = e - s
        per_total = 0.0
        if num > 0:
            per_total = (total / num)

        print ''
        print 'Path =', path
        print 'Count =', str(num)
        print 'Per-Insert Time = %.4g seconds' % per_total
        print 'Total Time = %.4g seconds' % total
        print 'Finished.'
        print '=' * 80


if __name__ == '__main__':
    main()
