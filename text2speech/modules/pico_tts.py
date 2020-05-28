import subprocess

from text2speech.modules import TTS, TTSValidator


class PicoTTS(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en-US"}
        super(PicoTTS, self).__init__(config, PicoTTSValidator(self))
        if self.lang.startswith("de"):
            self.voice = "de-DE"
        elif self.lang.startswith("es"):
            self.voice = "es-ES"
        elif self.lang.startswith("fr"):
            self.voice = "fr-FR"
        elif self.lang.startswith("it"):
            self.voice = "it-IT"
        elif self.lang.startswith("en"):
            self.voice = "en-US"
            if "gb" in self.lang.lower() or "uk" in self.lang.lower():
                self.voice = "en-GB"

    def get_tts(self, sentence, wav_file):
        subprocess.call(
            ['pico2wave', '-l', self.voice, "-w", wav_file, sentence])

        return wav_file, None

    def describe_voices(self):
        voices = {}
        for lang_code in ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR',
                          'it-IT']:
            voices[lang_code] = [lang_code]
        return voices


class PicoTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PicoTTSValidator, self).__init__(tts)

    def validate_connection(self):
        try:
            subprocess.call(['pico2wave', '--help'])
        except:
            raise Exception(
                'PicoTTS is not installed. Run: '
                '\nsudo apt-get install libttspico0\n'
                'sudo apt-get install  libttspico-utils')

    def get_tts_class(self):
        return PicoTTS
