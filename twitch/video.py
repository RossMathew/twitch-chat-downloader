import json
from pathlib import Path
from typing import List, Generator, Union
from twitch import InvalidInputFileException, TwitchAPI


class Video:
    def __init__(self, video_id: str = None, json_file_name: str = None):
        self.id: str = video_id
        self.twitch_api: TwitchAPI = TwitchAPI()
        self.json_file_name: str = json_file_name
        self.comments: Union[Generator[dict, None, None], List[dict]] = {}

        if json_file_name:
            if Path(json_file_name).is_file():
                with open(json_file_name, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    if all(key in json_data for key in ['video', 'comments']):
                        self.metadata = json_data['video']
                        self.comments = json_data['comments']
                    else:
                        raise InvalidInputFileException('Malformed input file.')
            else:
                raise InvalidInputFileException('Input file does not exist.')
        else:
            self.metadata = self.twitch_api.video(self.id)
            self.comments = self.twitch_api.comments(self.id)

    def __str__(self):
        if 'title' in self.metadata:
            return self.metadata['title']
        elif self.id:
            return self.id
        else:
            return 'Unknown video'

    def __eq__(self, other):
        return self.id == other.id
