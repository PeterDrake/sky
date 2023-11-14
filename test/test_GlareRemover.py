import unittest
import shutil
from pandas.testing import assert_frame_equal
from subprocess import check_output
from GlareRemover import *
from Preprocessor import Preprocessor

class TestGlareRemover(unittest.TestCase):

    def setUp(self):
        print('WARNING: Some of these tests only verify that the results of the preprocessing exist.')
        print('For a more thorough test, delete your test_data directory before running them.')
        self.glare_remover = GlareRemover('../test_data', verbose=True)

    def test_removes_glare_and_writes_files(self):
        # Ensure that the clean CSV file exists
        preprocessor = Preprocessor('../test_raw_data', '../test_raw_csv', '../test_data', verbose=False)
        preprocessor.write_clean_csv('tiny_data.csv')
        # Only do the expensive preprocessing if it hasn't already been done
        if not os.path.exists(timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20180418000200')):
            print('Doing expensive preprocessing of test files')
            self.glare_remover.preprocess_images('tiny_data.csv')
        # Now check if some of the files exist
        files = [timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20180418000200'),
                 timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20180419000200')]
        for f in files:
            self.assertTrue(os.path.exists(f))