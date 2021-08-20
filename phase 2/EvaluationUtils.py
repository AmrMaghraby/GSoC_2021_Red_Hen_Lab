import os
import numpy as np

from SceneBoundaryDetector import SceneBoundaryDetector
from typing import List


class EvaluationUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_video_file_name(video_file):
        return os.path.splitext(os.path.basename(video_file))[0]

    @staticmethod
    def pyscene_evaluator(threshold: int, video_files: List[str], results_files) -> np.array:
        number_of_videos = len(video_files)
        average_accuracy = 0
        for video_file in video_files:
            video_file_name = EvaluationUtils.get_video_file_name(video_file)
            print(video_file_name)
            if video_file_name in results_files:
                SceneBoundaryDetector.set_video_configuration(video_file)
                list_scene = SceneBoundaryDetector.find_scenes(threshold)
                results_file = results_files[video_file_name]
                accuracy = EvaluationUtils.calculate_accuracy(list_scene, results_file)
                average_accuracy = average_accuracy + accuracy
                number_of_videos = number_of_videos - 1
        average_accuracy = average_accuracy / number_of_videos
        return np.array([average_accuracy])

    @staticmethod
    def calculate_accuracy(list_scene, results_file):
        timecode_optimal_result = set([x[:8] for x in (results_file['Timecode'].tolist())])
        list_scene_ = set([x[1].get_timecode()[:8] for x in list_scene][:-1])
        number_of_union_optimal_results_and_detected_results = len(timecode_optimal_result.union(list_scene_))
        number_of_intersection_optimal_results_and_detected_results = len(
            timecode_optimal_result.intersection(list_scene_))
        return number_of_intersection_optimal_results_and_detected_results \
               / number_of_union_optimal_results_and_detected_results