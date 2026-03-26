from utils.enums import TestParam

import unittest
import test_source1_scraper
import test_source1_detail_scraper
import test_cleanData
import test_loaders

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if TestParam.TEST_SOURCE_1:
        suite.addTests(loader.loadTestsFromModule(test_source1_scraper))
    
    if TestParam.TEST_SOURCE_1_DETAIL:
        suite.addTests(loader.loadTestsFromModule(test_source1_detail_scraper))

    if TestParam.TEST_CLEAN:
        suite.addTests(loader.loadTestsFromModule(test_cleanData))

    if TestParam.TEST_LOADERS:
        suite.addTests(loader.loadTestsFromModule(test_loaders))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
