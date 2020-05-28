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
import requests

from text2speech.modules import RemoteTTS, TTSValidator


class MaryTTS(RemoteTTS):
    PARAMS = {
        'INPUT_TYPE': 'TEXT',
        'AUDIO': 'WAVE_FILE',
        'OUTPUT_TYPE': 'AUDIO'
    }

    def __init__(self, config=None):
        config = config or {"lang": "en-us",
                            "url": "http://mary.dfki.de:59125/",
                            "voice": 'cmu-bdl-hsmm'
                            }
        super(MaryTTS, self).__init__(config, api_path='/process',
                                      validator=MaryTTSValidator(self))

        if self.lang.lower() in ["en-uk", "en-gb"]:
            self.lang = "en_GB"
        elif self.lang.lower().startswith("en"):
            self.lang = "en_US"

    def build_request_params(self, sentence):
        params = self.PARAMS.copy()
        params['LOCALE'] = self.lang
        params['VOICE'] = self.voice
        params['INPUT_TEXT'] = sentence.encode('utf-8')
        return params

    def describe_voices(self):
        voices = {}
        locales = requests.get(self.url + "/locales").text.split()
        for l in locales:
            voices[l] = []
        voice_data = requests.get(self.url + "/voices").text.split("\n")
        for v in voice_data:
            if not v.strip():
                continue
            voice, lang_code, gender = v.split()[:3]
            voices[lang_code] += [voice]
        return voices


class MaryTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(MaryTTSValidator, self).__init__(tts)

    def validate_connection(self):
        try:
            resp = requests.get(self.tts.url + "/version", verify=False)
            if not resp.text.startswith("Mary TTS server"):
                raise Exception('Invalid MaryTTS server.')
        except:
            raise Exception(
                'MaryTTS server could not be verified. Check your connection '
                'to the server: ' + self.tts.url)

    def get_tts_class(self):
        return MaryTTS
