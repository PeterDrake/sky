import unittest
from ExperimentLogUpdater import *


class TestExperimentLogUpdater(unittest.TestCase):

    def setUp(self):
        self.updater = ExperimentLogUpdater('../test_results', 'test_experiment', False)

    def test_loads_log(self):
        log = self.updater.load_or_create_log_dataframe()
        self.assertEqual(['name', 'date', 'githash', 'netfile', 'notes'], list(log.columns))

    def test_detects_experiment_name_not_in_empty_log_file(self):
        os.remove(self.updater.log_filename)
        self.updater.log = self.updater.load_or_create_log_dataframe()
        self.assertFalse(self.updater.experiment_name_in_use())

    def test_detects_experiment_name_not_in_use(self):
        self.updater.log = self.updater.load_or_create_log_dataframe()
        self.updater.add_log_line('dummy date', 'dummy git hash')
        self.updater.write_log_file()
        # Replace the updater with one using a different experiment name
        self.updater = ExperimentLogUpdater('../test_results', 'test_experiment2', False)
        # That name should now NOT be in use
        self.updater.log = self.updater.load_or_create_log_dataframe()
        self.assertFalse(self.updater.experiment_name_in_use())

    def test_detects_experiment_name_in_use(self):
        self.updater.log = self.updater.load_or_create_log_dataframe()
        self.updater.add_log_line('dummy date', 'dummy git hash')
        self.updater.write_log_file()
        self.updater.log = self.updater.load_or_create_log_dataframe()
        # The log should now contain the name we're trying to re-use
        self.assertTrue(self.updater.experiment_name_in_use())

    def test_creates_experiment_directory_when_it_does_not_exist(self):
        path = self.updater.results_dir + '/' + self.updater.experiment_name
        shutil.rmtree(path, ignore_errors=True)
        self.updater.create_experiment_directory()
        self.assertTrue(os.path.isdir(path))

    def test_replaces_experiment_directory_when_it_does_exist(self):
        path = self.updater.results_dir + '/' + self.updater.experiment_name
        self.updater.create_experiment_directory()
        file = path + '/junk.txt'  # Create a junk file
        with open(file, 'a'):
            pass
        self.updater.create_experiment_directory()
        self.assertEqual([], os.listdir(path))


if __name__ == '__main__':
    unittest.main()
