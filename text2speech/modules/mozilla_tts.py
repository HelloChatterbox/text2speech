import requests
from text2speech.modules import TTS, TTSValidator


class MozillaTTSServer(TTS):
    works_offline = False
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"url": "http://0.0.0.0:5002"}
        super(MozillaTTSServer, self).__init__(config, MozillaTTSValidator(self),
                                               ssml_tags=[])
        self.url = config['url']
        self.type = 'wav'

    def get_tts(self, sentence, wav_file):
        response = requests.get(self.url + "/api/tts", params={"text": sentence})
        with open(wav_file, 'wb') as f:
            f.write(response.content)
        return (wav_file, None)  # No phonemes


class MozillaTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MozillaTTSValidator, self).__init__(tts)

    def validate_dependencies(self):
        pass

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        url = self.tts.config['url']
        response = requests.get(url)
        if not response.status_code == 200:
            raise ConnectionRefusedError

    def get_tts_class(self):
        return MozillaTTSServer
