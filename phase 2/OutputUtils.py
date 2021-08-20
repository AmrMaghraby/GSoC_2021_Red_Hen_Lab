import os
import json

from datetime import datetime
from EvaluationUtils import EvaluationUtils


class OutputUtils:
    notation_template = dict()
    item_template = dict()

    notation_template["@context"] = [
        "http://www.w3.org/ns/anno.jsonld",
        "http://iiif.io/api/presentation/3/context.json"
    ]

    notation_template["service"] = [
        {
            "id": "https://github.com/tre3x/FilmEditDetection",
            "type": "CutDetector",
            "client_id": "FilmEditDetector",
            "client_ver": "0.0.1"
        }
    ]

    notation_template["type"] = "Manifest"
    notation_template["rights"] = "http://creativecommons.org/licenses/by/4.0/"
    notation_template["label"] = {
        "en": []
    }

    notation_template["items"] = {
        "type": "AnnotationPage"
    }

    item_template["type"] = "Annotation"
    item_template["generator"] = "https://github.com/tre3x/FilmEditDetection"
    item_template["motivation"] = "highlighting"
    item_template["creator"] = {
        "type": "Agent",
        "nickname": "FilmEditDetector"
    }
    item_template["rights"] = "http://creativecommons.org/licenses/by/4.0/"
    item_template["target"] = {
        "type": "SpecificResource",
        "selector": {
            "type": "FragmentSelector",
            "conformsTo": "http://www.w3.org/TR/media-frags/"
        }
    }

    @staticmethod
    def output_json(video_file, scenes_list, scene_width, scene_height, scene_duration):
        item = OutputUtils.item_template.copy()
        constants = OutputUtils.notation_template.copy()
        constants["items"] = [dict()]
        constants["items"][0]["content"] = [dict()]
        constants["items"][0]["content"][0]["label"] = dict()
        now = datetime.now()
        video_file_name=EvaluationUtils.get_video_file_name(video_file)

        constants["id"] = "file://"+os.getcwd()+"/output/"+video_file_name+".json"
        constants["label"]["en"].append("Annotations for \"{}\"".format(video_file_name))
        constants["items"][0]["id"] = "file://"+os.getcwd()+"/output/"+video_file_name+".json#canvas"
        constants["items"][0]["type"] = "Canvas"
        constants["items"][0]["height"] = scene_height
        constants["items"][0]["width"] = scene_width
        constants["items"][0]["duration"] = scene_duration
        constants["items"][0]["content"][0]["id"] = "file://"+video_file
        constants["items"][0]["content"][0]["type"] = "Video"
        constants["items"][0]["content"][0]["height"] = scene_height
        constants["items"][0]["content"][0]["width"] = scene_width
        constants["items"][0]["content"][0]["duration"] = scene_duration
        constants["items"][0]["content"][0]["label"]["en"] = [video_file_name]
        constants["items"][0]["content"][0]["description"] = dict()

        constants["items"][0]["items"] = [dict()]
        constants["items"][0]["items"][0]["id"] = "file://"+os.getcwd()+"/output/"+video_file_name+".json#annotations"
        constants["items"][0]["items"][0]["type"] = "AnnotationPage"
        constants["items"][0]["items"][0]["items"] = []

        for scene_number, scene_list in enumerate(scenes_list):
            item = OutputUtils.item_template.copy()
            item["id"] = "file://"+os.getcwd()+"/output/"+video_file_name+".json#scene"+str(scene_number)
            item["created"] = now.strftime("%Y-%m-%d %H:%M:%S")
            item["target"] = dict()
            item["target"]["source"] = "file://"+video_file
            item["target"]["type"] = "SpecificResource"
            item["target"]["selector"] = dict()
            item["target"]["selector"]["type"] = "FragmentSelector"
            item["target"]["selector"]["conformsTo"] = "http://www.w3.org/TR/media-frags/"
            item["target"]["selector"]["value"] = "t="+str(scene_list[0].get_seconds())+","\
                                                  + str(scene_list[1].get_seconds())

            constants["items"][0]["items"][0]["items"].append(item)

        print(json.dumps(constants, indent=4))
        OutputUtils.create_output_directory_if_not_exist()
        print(os.getcwd())
        with open('output/'+video_file_name+'.json', 'w') as output_file:
            output_file.write(json.dumps(constants, indent=4))

    @staticmethod
    def create_output_directory_if_not_exist():
        os.makedirs('output', exist_ok=True)

