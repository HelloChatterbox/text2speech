# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
