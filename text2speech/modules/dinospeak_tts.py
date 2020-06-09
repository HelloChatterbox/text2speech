# Copyright 2020 Chatterbox
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


class DinoSpeakTTS(TTS):

    def __init__(self, config=None):
        config = config or {
            "base_tts":
                {"module": "espeak",
                 "lang": "en-us",
                 "voice": "croak"}
        }
        from text2speech import TTSFactory
        global DinoEncoder
        from dinospeak.dinospeak import DinoEncoder
        self.base_tts = TTSFactory.create(config["base_tts"])
        super(DinoSpeakTTS, self).__init__(config, DinoSpeakValidator(self),
                                           ssml_tags=["speak", "say-as",
                                                      "voice",
                                                      "audio", "prosody",
                                                      "break",
                                                      "emphasis", "sub",
                                                      "tts:style", "p", "s",
                                                      "mark"])

    def get_tts(self, sentence, wav_file):
        sentence = DinoEncoder().encode(sentence)
        return self.base_tts.get_tts(sentence, wav_file)

    def describe_voices(self):
        return self.base_tts.describe_voices()


class DinoSpeakValidator(TTSValidator):
    def __init__(self, tts):
        super(DinoSpeakValidator, self).__init__(tts)

    def validate_dependencies(self):
        from dinospeak.dinospeak import DinoEncoder

    def validate_connection(self):
        return self.tts.base_tss.validate()

    def get_tts_class(self):
        return DinoSpeakTTS
