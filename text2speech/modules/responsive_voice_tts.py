import requests
from ovos_utils.log import LOG
from text2speech.modules import TTS, TTSValidator
from responsive_voice import ResponsiveVoice
from responsive_voice import get_voices


class ResponsiveVoiceTTS(TTS):
    works_offline = False
    audio_ext = "mp3"

    def __init__(self, config=None):
        config = config or {"lang": "en",
                            "pitch": 0.5,
                            "rate": 0.5,
                            "vol": 1}
        super().__init__(config, validator=ResponsiveVoiceValidator(self),
                         ssml_tags=[])
        self.clear_cache()
        self.pitch = config.get("pitch", 0.5)
        self.rate = config.get("rate", 0.5)
        self.vol = config.get("vol", 1)

        if self.voice:
            clazz = get_voices()[self.voice]
            self.engine = clazz(pitch=self.pitch, rate=self.rate, vol=self.vol)
        else:
            gender = config.get("gender", "male")
            self.engine = ResponsiveVoice(lang=self.lang, gender=gender,
                                          pitch=self.pitch, rate=self.rate,
                                          vol=self.vol)

    def get_tts(self, sentence, wav_file):
        self.engine.get_mp3(sentence, wav_file)
        return (wav_file, None)  # No phonemes

    def describe_voices(self):
        voice_clazzes = get_voices()
        voices = {}
        for voice in voice_clazzes:
            lang = voice_clazzes[voice]().lang.split("_#")[0]
            if lang not in voices:
                voices[lang] = []
            if lang.split("-")[0] not in voices:
                voices[lang.split("-")[0]] = []
            voices[lang].append(voice)
            voices[lang.split("-")[0]].append(voice)
        return voices


class ResponsiveVoiceValidator(TTSValidator):
    def __init__(self, tts):
        super(ResponsiveVoiceValidator, self).__init__(tts)

    def validate_voice(self):
        if self.tts.voice is not None:
            super().validate_voice()

    def validate_connection(self):
        r = requests.get("https://responsivevoice.org")
        if r.status_code == 200:
            return True
        LOG.warning("Could not reach https://responsivevoice.org")

    def get_tts_class(self):
        return ResponsiveVoiceTTS
