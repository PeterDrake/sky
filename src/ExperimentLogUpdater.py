from config import *
import os
import pandas as pd


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
            self.crash(EXPERIMENT_NAME + ' is already in results/experiment_log.csv; manually delete it or change the name in config.py')
        date = date.today()
        repo = git.Repo(search_parent_directories=True)
        # TODO Uncomment this!
        # if repo.is_dirty(untracked_files=True):
        #     print('Not in a clean git state! Commit or revert.')
        #     sys.exit()
        git_hash = repo.head.object.hexsha
        self.add_log_line(date, git_hash)
        self.write_log_file()


        # Create directory for this experiment
        experiment_directory = '../results/' + EXPERIMENT_NAME
        os.makedirs(experiment_directory, exist_ok=True)
        # TODO Destroy any existing directory for this experiment name

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
