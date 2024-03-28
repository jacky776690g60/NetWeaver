import unittest

from pytools import Logger, LogLevel

if __name__ == '__main__':
    logger = Logger(LogLevel.ERROR)
    logger.info("Running all test scripts...")
    
    loader = unittest.TestLoader()      #NOTE: This will discover and run all tests in the tests directory
    start_dir = 'tests'                 #NOTE: Path to your test files
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)