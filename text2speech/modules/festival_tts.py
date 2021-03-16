import subprocess
from text2speech.modules import TTS, TTSValidator


class FestivalTTS(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en-us"}
        super().__init__(config, FestivalValidator(self), ssml_tags=[])

    def get_tts(self, sentence, wav_file):
        subprocess.call('echo "{utt}" | text2wave -o {wave}'.format(
            utt=sentence, wave=wav_file), shell=True)
        return wav_file, None

    def describe_voices(self):
        voices = {}  # TODO
        return voices


class FestivalValidator(TTSValidator):
    def validate_voice(self):
        pass  # TODO

    def validate_lang(self):
        pass  # TODO

    def validate_connection(self):
        try:
            subprocess.call(["text2wave", "-h"])
        except:
            raise Exception(
                'Festival not installed. Run sudo apt-get install festival')

    def get_tts_class(self):
        return FestivalTTS
