from gtts import gTTS
from gtts.lang import tts_langs
from text2speech.modules import TTS, TTSValidator
from ovos_utils.log import LOG

import logging
logging.getLogger('gtts.tts').setLevel(logging.CRITICAL)
logging.getLogger("gtts.lang").setLevel(logging.CRITICAL)


class GoogleTTS(TTS):
    works_offline = False
    audio_ext = "mp3"
    _default_langs = {'af': 'Afrikaans', 'sq': 'Albanian', 'ar': 'Arabic',
                      'hy': 'Armenian', 'bn': 'Bengali', 'bs': 'Bosnian',
                      'ca': 'Catalan', 'hr': 'Croatian', 'cs': 'Czech',
                      'da': 'Danish', 'nl': 'Dutch', 'en': 'English',
                      'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino',
                      'fi': 'Finnish', 'fr': 'French', 'de': 'German',
                      'el': 'Greek', 'gu': 'Gujarati', 'hi': 'Hindi',
                      'hu': 'Hungarian', 'is': 'Icelandic', 'id': 'Indonesian',
                      'it': 'Italian', 'ja': 'Japanese', 'jw': 'Javanese',
                      'kn': 'Kannada', 'km': 'Khmer', 'ko': 'Korean',
                      'la': 'Latin', 'lv': 'Latvian', 'mk': 'Macedonian',
                      'ml': 'Malayalam', 'mr': 'Marathi',
                      'my': 'Myanmar (Burmese)', 'ne': 'Nepali',
                      'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
                      'ro': 'Romanian', 'ru': 'Russian', 'sr': 'Serbian',
                      'si': 'Sinhala', 'sk': 'Slovak', 'es': 'Spanish',
                      'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
                      'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
                      'tr': 'Turkish',
                      'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
                      'cy': 'Welsh', 'zh-cn': 'Chinese (Mandarin/China)',
                      'zh-tw': 'Chinese (Mandarin/Taiwan)',
                      'en-us': 'English (US)', 'en-ca': 'English (Canada)',
                      'en-uk': 'English (UK)', 'en-gb': 'English (UK)',
                      'en-au': 'English (Australia)',
                      'en-gh': 'English (Ghana)',
                      'en-in': 'English (India)', 'en-ie': 'English (Ireland)',
                      'en-nz': 'English (New Zealand)',
                      'en-ng': 'English (Nigeria)',
                      'en-ph': 'English (Philippines)',
                      'en-za': 'English (South Africa)',
                      'en-tz': 'English (Tanzania)',
                      'fr-ca': 'French (Canada)',
                      'fr-fr': 'French (France)',
                      'pt-br': 'Portuguese (Brazil)',
                      'pt-pt': 'Portuguese (Portugal)',
                      'es-es': 'Spanish (Spain)',
                      'es-us': 'Spanish (United States)'
                      }

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
            try:
                langs = tts_langs()
            except:
                langs = self._default_langs
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
