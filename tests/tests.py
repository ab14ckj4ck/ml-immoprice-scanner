import unittest
import test_source1_scraper
import test_source1_detail_scraper
import test_cleanData
import test_loaders

TEST_SOURCE_1 = True
TEST_SOURCE_1_DETAIL = True
TEST_CLEAN = True
TEST_LOADERS = True

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    if TEST_SOURCE_1:
        suite.addTests(loader.loadTestsFromModule(test_source1_scraper))
    
    if TEST_SOURCE_1_DETAIL:
        suite.addTests(loader.loadTestsFromModule(test_source1_detail_scraper))

    if TEST_CLEAN:
        suite.addTests(loader.loadTestsFromModule(test_cleanData))

    if TEST_LOADERS:
        suite.addTests(loader.loadTestsFromModule(test_loaders))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
