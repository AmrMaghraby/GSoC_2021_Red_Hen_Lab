from scenedetect import ContentDetector, SceneManager, VideoManager


class SceneBoundaryDetector:
    def __init__(self):
        pass

    def set_video_configuration(self, video_file_path):
        self.video_manager = VideoManager([video_file_path])
        self.scene_manager = SceneManager()

    def find_scenes(self, threshold=30.0):
        # Create our scene managers, then add the detector.
        self.scene_manager.add_detector(
            ContentDetector(threshold=threshold))

        # Improve processing speed by downscaling before processing.
        self.video_manager.set_downscale_factor()

        # Start the video manager and perform the scene detection.
        self.video_manager.start()

        self.scene_manager.detect_scenes(frame_source=self.video_manager)

        # Each returned scene is a tuple of the (start, end) timecode.
        return self.scene_manager.get_scene_list()

    def get_video_file_frame_size(self):
        # get the width and the height of each video
        return self.video_manager.get_framesize()

    def get_video_file_duration(self):
        # get video duration in seconds
        return self.video_manager.get_duration()[0].get_seconds()

