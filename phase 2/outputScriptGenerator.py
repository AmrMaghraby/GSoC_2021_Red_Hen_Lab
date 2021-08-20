import argparse

from OutputUtils import OutputUtils
from SceneBoundaryDetector import SceneBoundaryDetector


def format_generator():
    parser = argparse.ArgumentParser(description="Input for running pyScene tool")
    parser.add_argument("video_file", type=str, help="File path for the video input")
    parser.add_argument("--output-json", action='store_false', help="outputs result in JSON format")
    parser.add_argument("--output-csv", action='store_false', help="outputs result in CSV format")
    args = parser.parse_args()
    video_file = args.video_file
    is_json = args.output_json
    is_csv = args.output_csv

    scene_boundary_detector = SceneBoundaryDetector()
    scene_boundary_detector.set_video_configuration(video_file)
    scene_list = scene_boundary_detector.find_scenes()
    scene_width, scene_height = scene_boundary_detector.get_video_file_frame_size()
    scene_duration = scene_boundary_detector.get_video_file_duration()

    OutputUtils.output_json(video_file, scene_list, scene_width, scene_height, scene_duration)
    #print(scene_list)


if __name__ == '__main__':
    format_generator()
