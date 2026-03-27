from utils.enums import TestParam

import unittest
import test_austriaFeatureEngineering
import test_db_insertion

# These are imported in the original tests.py, but might be missing/renamed
try:
    import test_source1_scraper
    HAS_SOURCE1 = True
except ImportError:
    HAS_SOURCE1 = False

try:
    import test_source1_detail_scraper
    HAS_SOURCE1_DETAIL = True
except ImportError:
    HAS_SOURCE1_DETAIL = False

try:
    import test_cleanData
    HAS_CLEAN = True
except ImportError:
    HAS_CLEAN = False

try:
    import test_loaders
    HAS_LOADERS = True
except ImportError:
    HAS_LOADERS = False

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if TestParam.TEST_SOURCE_1 and HAS_SOURCE1:
        suite.addTests(loader.loadTestsFromModule(test_source1_scraper))
    
    if TestParam.TEST_SOURCE_1_DETAIL and HAS_SOURCE1_DETAIL:
        suite.addTests(loader.loadTestsFromModule(test_source1_detail_scraper))

    if TestParam.TEST_CLEAN and HAS_CLEAN:
        suite.addTests(loader.loadTestsFromModule(test_cleanData))

    if TestParam.TEST_LOADERS and HAS_LOADERS:
        suite.addTests(loader.loadTestsFromModule(test_loaders))

    if TestParam.TEST_AUSTRIA_FE:
        suite.addTests(loader.loadTestsFromModule(test_austriaFeatureEngineering))

    if TestParam.TEST_DB:
        suite.addTests(loader.loadTestsFromModule(test_db_insertion))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
