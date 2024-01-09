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
        self.glare_remover = GlareRemover('../test_data', '../test_raw_csv', verbose=True)

    def test_writes_deglared_files(self):
        # Only do the expensive preprocessing if it hasn't already been done
        if not os.path.exists(timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20180418000200')):
            print('Doing expensive preprocessing of test files')
            self.glare_remover.create_image_directories('tiny_tsi_fsc.csv')
            self.glare_remover.write_deglared_files('tiny_tsi_fsc.csv')
        # TODO Verify that some files with glare are also copied
        # Now check if some of the files exist
        files = [timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20160525160000'),
                 timestamp_to_tsi_mask_no_glare_path(self.glare_remover.data_dir, '20170524173100')]
        for f in files:
            self.assertTrue(os.path.exists(f))