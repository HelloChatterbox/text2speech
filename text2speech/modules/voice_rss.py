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
from text2speech.modules import TTS, TTSValidator
import requests


class VoiceRSSTTS(TTS):
    audio_ext = "mp3"

    def __init__(self, config=None):
        config = config or {"lang": "en-us",
                            "voice": "English (United States)"}
        super().__init__(config, VoiceRSSValidator(self), ssml_tags=[])
        self.key = self.config.get("key")
        if not self.voice:
            self.voice = self.describe_voices()[self.lang][0]

    def __speech(self, settings):
        self.__validate(settings)
        return self.__request(settings)

    def __validate(self, settings):
        if not settings: raise RuntimeError('The settings are undefined')
        if 'key' not in settings or not settings['key']: raise RuntimeError(
            'The API key is undefined')
        if 'src' not in settings or not settings['src']: raise RuntimeError(
            'The text is undefined')
        if 'hl' not in settings or not settings['hl']: raise RuntimeError(
            'The language is undefined')

    def __request(self, settings):
        result = {'error': None, 'response': None}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        params = self.__buildRequest(settings)
        url = "https://api.voicerss.org:443"
        response = requests.post(url, '/', params=params, headers=headers)

        content = response.text

        if response.status_code != 200:
            result['error'] = response.reason
        elif content.find('ERROR') == 0:
            result['error'] = content
        else:
            result['response'] = content
            return bytes(response.content)
        return result

    def __buildRequest(self, settings):
        params = {'key': '', 'src': '', 'hl': '', 'r': '', 'c': '', 'f': '',
                  'ssml': '', 'b64': ''}

        if 'key' in settings: params['key'] = settings['key']
        if 'src' in settings: params['src'] = settings['src']
        if 'hl' in settings: params['hl'] = settings['hl']
        if 'r' in settings: params['r'] = settings['r']
        if 'c' in settings: params['c'] = settings['c']
        if 'f' in settings: params['f'] = settings['f']
        if 'ssml' in settings: params['ssml'] = settings['ssml']
        if 'b64' in settings: params['b64'] = settings['b64']

        return params

    def get_tts(self, sentence, wav_file):
        bin_data = self.__speech({
            'key': self.key,
            'hl': self.lang,
            'src': sentence,
            'r': '0',
            'c': self.audio_ext,
            'f': '44khz_16bit_stereo',
            'ssml': 'false',
            'b64': 'false'
        })
        with open(wav_file, "wb") as f:
            f.write(bin_data)
        return wav_file, None

    def describe_voices(self):
        voices = {"ca-es": ["Catalan"],
                  "zh-cn": ["Chinese (China)"],
                  "zh-hk": ["Chinese (Hong Kong)"],
                  "zh-tw": ["Chinese (Taiwan)"],
                  "da-dk": ["Danish"],
                  "nl-nl": ["Dutch"],
                  "en-au": ["English (Australia)"],
                  "en-ca": ["English (Canada)"],
                  "en-gb": ["English (Great Britain)"],
                  "en-in": ["English (India)"],
                  "en-us": ["English (United States)"],
                  "fi-fi": ["Finnish"],
                  "fr-ca": ["French (Canada)"],
                  "fr-fr": ["French (France)"],
                  "de-de": ["German"],
                  "it-it": ["Italian"],
                  "ja-jp": ["Japanese"],
                  "ko-kr": ["Korean"],
                  "nb-no": ["Norwegian"],
                  "pl-pl": ["Polish"],
                  "pt-br": ["Portuguese (Brazil)"],
                  "pt-pt": ["Portuguese (Portugal)"],
                  "ru-ru": ["Russian"],
                  "es-mx": ["Spanish (Mexico)"],
                  "es-es": ["Spanish (Spain)"],
                  "sv-se": ["Swedish (Sweden)"]}
        return voices


class VoiceRSSValidator(TTSValidator):

    def validate_connection(self):
        assert self.tts.key is not None

    def get_tts_class(self):
        return VoiceRSSTTS

