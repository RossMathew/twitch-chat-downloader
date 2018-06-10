import argparse
from .singleton import Singleton
from .config import Config


class CLI(metaclass=Singleton):
    def __init__(self):
        self.arguments = self.get_arguments()
        print(Config().filename)
        Config().load(self.arguments.settings)
        Config().save()

        # Video ID
        if self.arguments.video is None and self.arguments.input is None:
            self.arguments.video = self.prompt_video_id()

        # Client ID
        if Config().data['client_id'] is None and self.arguments.client_id is None:
            self.arguments.client_id = self.prompt_client_id()

        # New client ID
        if Config().data['client_id'] is not self.arguments.client_id:
            Config().data['client_id'] = self.arguments.client_id.strip()
            if not input('Save client ID? (Y/n): ').lower().startswith('n'):
                Config().save()

    @staticmethod
    def get_arguments():
        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description='Twitch Chat Downloader v{version}'.format(version=Config().data['version']))

        parser.add_argument('-v', '--video', type=str, help='Video id')
        # parser.add_argument('-c', '--channel', type=str, help='Channel name')
        # parser.add_argument('--limit', type=int, help='Number of videos from channel')
        parser.add_argument('--client_id', type=str, help='Twitch client id')
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('-q', '--quiet', action='store_true')
        parser.add_argument('-o', '--output', type=str, help='Output folder', default=Config().data['default_output'])
        parser.add_argument('-f', '--format', type=str, help='Message format', default=Config().data['default_format'])
        # parser.add_argument('--start', type=int, help='Start time in seconds from video start')
        # parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
        parser.add_argument('--settings', type=str, help='Settings file', default=Config().SETTINGS_FILE_NAME)
        parser.add_argument('--timezone', type=str, help='Timezone name')
        parser.add_argument('--init', action='store_true', help='Script setup')
        parser.add_argument('--update', action='store_true', help='Update settings')
        parser.add_argument('--version', action='store_true', help='Settings version')
        parser.add_argument('--formats', action='store_true', help='List available formats')
        parser.add_argument('--preview', action='store_true', help='Print chat lines')
        parser.add_argument('--input', type=str, help='Read data from JSON file')

        return parser.parse_args()

    @staticmethod
    def prompt_video_id() -> str:
        return input('Video ID: ').strip('v')

    @staticmethod
    def prompt_client_id() -> str:
        print('Twitch requires a client ID to use their API.'
              '\nRegister an application on https://dev.twitch.tv/dashboard to get yours.')
        return input('Client ID: ').strip()

    @staticmethod
    def print_version():
        print(Config().version())

    def print_format_list(self):
        if self.arguments.formats:
            for format_name in Config().data['formats']:
                print(format_name)
                format_dictionary = Config().data['formats'][format_name]
                if 'comments' in format_dictionary:
                    print('\tcomment: {}'.format(Config().data['formats'][format_name]['comments']['format']))
                if 'output' in format_dictionary:
                    print('\toutput: {}'.format(Config().data['formats'][format_name]['output']['format']))
                print('\n')

    @staticmethod
    def initialize_settings_file():
        Config().save()
        exit()
