import glob
import os
import pandas as pd

from typing import List


class InputUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_files(file_type, file_dir) -> List[str]:
        return list(glob.iglob(file_dir + '*.' + file_type))

    @staticmethod
    def read_files(data_dir):
        optimal_results_files = InputUtils.get_files('csv', data_dir)
        optimal_results_dataframe_dictionary = dict()
        for optimal_results_file in optimal_results_files:
            optimal_results_data_frame = pd.read_csv(optimal_results_file)
            video_file_name = os.path.splitext(os.path.basename(optimal_results_file))[0]
            video_file_name = video_file_name.replace(' v2 - Sheet1', '')
            optimal_results_dataframe_dictionary[video_file_name] = optimal_results_data_frame
        return optimal_results_dataframe_dictionary
