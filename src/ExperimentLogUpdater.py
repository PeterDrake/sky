from config import *
import os
import pandas as pd
from datetime import date
import git
import sys
import shutil


class GitError(Exception):
    """Thrown if we try to run an experiment when not in a clean git state."""
    pass


class ExperimentNameInUseError(Exception):
    """Thrown if we try to use an experiment name that has been used."""
    pass


class ExperimentLogUpdater:

    def __init__(self, results_dir, experiment_name, insist_on_clean_git_state):
        self.results_dir = results_dir
        self.experiment_name = experiment_name
        self.log_filename = self.results_dir + '/experiment_log.csv'
        self.insist_on_clean_git_state = insist_on_clean_git_state
        self.log = 'Not yet defined'

    def update(self):
        self.log = self.load_or_create_log_dataframe()
        if self.experiment_name_in_use():
            raise ExperimentNameInUseError(self.experiment_name + ' is already in results/experiment_log.csv; manually delete it or change the name in config.py')
        self.add_log_line(date.today(), self.get_git_hash())
        self.write_log_file()
        self.create_experiment_directory()

    def get_git_hash(self):
        """
        Returns the current git state hash, or crashes if not in a clean git state (i.e., there are uncommitted changes).
        :return:
        """
        repo = git.Repo(search_parent_directories=True)
        if self.insist_on_clean_git_state and repo.is_dirty(untracked_files=True):
            raise GitError('Not in a clean git state! Commit or revert.')
        git_hash = repo.head.object.hexsha
        return git_hash

    def load_or_create_log_dataframe(self):
        """
        Loads the experiment log as a dataframe, or creates an empty one if it does not exist.
        :return: The log dataframe.
        """
        if os.path.isfile(self.log_filename):
            return pd.read_csv(self.log_filename)
        return pd.DataFrame(columns=['name', 'date', 'githash', 'netfile', 'notes'])

    def experiment_name_in_use(self):
        """
        Returns True if the current experiment name already has an entry in log.
        """
        return (self.log['name'] == self.experiment_name).any()

    @staticmethod
    def crash(self, message):
        """
        Prints message and exits.
        """
        print(message)
        sys.exit()

    def write_log_file(self):
        """
        Writes the log to experiment_log.csv in results_dir.
        """
        os.makedirs(self.results_dir, exist_ok=True)
        self.log.to_csv(self.log_filename, index=False)

    def add_log_line(self, date, git_hash):
        """
        Adds a line for the current experiment to the log. Note that write_log_file must still be called.
        """
        # TODO Also get the network filename as an argument
        self.log.loc[len(self.log)] = [self.experiment_name, date, git_hash, 'Some network file name', '']

    def create_experiment_directory(self):
        """
        Create an empty directory for this experiment, deleting any existing one. We would only have an existing
        directory if we had manually removed a line from the log file because, e.g., we started an experiment and
        immediately realized it should be abandoned due to some setup error.
        """
        path = self.results_dir + '/' + self.experiment_name
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
