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
from gtts import gTTS
from gtts.lang import tts_langs
from text2speech.modules import TTS, TTSValidator
from jarbas_utils.log import LOG

import logging
logging.getLogger('gtts.tts').setLevel(logging.CRITICAL)


class GoogleTTS(TTS):
    works_offline = False
    audio_ext = "mp3"

    def __init__(self, config=None):
        config = config or {"module": "google",
                            "lang": "en-us"}
        super(GoogleTTS, self).__init__(config, GoogleTTSValidator(self))
        self._voices = None
        voices = self.describe_voices()
        if self.lang not in voices and self.lang.split("-")[0] in voices:
            self.lang = self.lang.split("-")[0]

        self.voice = self.describe_voices()[self.lang][0]

    def get_tts(self, sentence, wav_file):
        tts = gTTS(sentence, lang=self.lang)
        tts.save(wav_file)
        return (wav_file, None)  # No phonemes

    def describe_voices(self):
        if self._voices is None:
            self._voices = {}
            langs = tts_langs()
            for lang_code in langs:
                self._voices[lang_code] = [langs[lang_code]]
        return self._voices


class GoogleTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(GoogleTTSValidator, self).__init__(tts)

    def validate_lang(self):
        assert self.tts.lang in self.tts.describe_voices()

    def validate_connection(self):
        try:
            gTTS(text='Hi')
        except:
            LOG.warning(
                'GoogleTTS server could not be verified. Please check your '
                'internet connection.')

    def get_tts_class(self):
        return GoogleTTS
