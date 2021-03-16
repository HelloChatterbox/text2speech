from text2speech.modules import TTS, TTSValidator
from voxpopuli import Voice
from tempfile import gettempdir
from os.path import join
from text2speech.util import LOG
from text2speech.visimes import ipa2arpabet


class MbrolaTTS(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en"}
        super(MbrolaTTS, self).__init__(config, MbrolaValidator(self))
        # TODO ssml tags ?
        self.lang = self.lang.split("-")[0]
        self.speed = self.config.get("speed", 160)  # word per minute
        self.pitch = self.config.get("pitch", 50)
        self.volume = self.config.get("volume")  # float 0 - 1
        self.voice_id = self.config.get("voice_id")

    def get_tts(self, sentence, wav_file):
        wav_file = self._get_wav(sentence, wav_file)
        #phoneme_list = self._get_phonemes(sentence)
        #phones = " ".join([":".join(pho) for pho in phoneme_list])
        phones = None
        return wav_file, phones

    def describe_voices(self):
        return self.get_voice().listvoices()

    def get_voice(self):
        return Voice(lang=self.lang, pitch=self.pitch, speed=self.speed,
                     voice_id=self.voice_id, volume=self.volume)

    def _get_phonemes(self, utterance, arpabet=False):
        voice = self.get_voice()
        if arpabet:
            return [(ipa2arpabet(phoneme.name), phoneme.duration) for
                    phoneme in voice.to_phonemes(utterance)]
        else:
            return [(phoneme.name, phoneme.duration) for
                    phoneme in voice.to_phonemes(utterance)]

    def _get_wav(self, utterance, out_file=None):
        voice = self.get_voice()
        wav = voice.to_audio(utterance)
        if out_file is None:
            out_file = join(gettempdir(), "voxpopuli.wav")
        with open(out_file, "wb") as wavfile:
            wavfile.write(wav)
        return out_file


class MbrolaValidator(TTSValidator):
    def __init__(self, tts):
        super(MbrolaValidator, self).__init__(tts)

    def validate_lang(self):
        langs = self.tts.describe_voices()
        if self.tts.lang not in langs:
            LOG.error("Unsupported language, choose one of {langs}".
                      format(langs=list(langs.keys())))
            raise ValueError
        if self.tts.voice_id is not None:
            if self.tts.voice_id not in langs[self.tts.lang]:
                LOG.error("Unsupported voice id, choose one of {langs} or "
                          "unset this value to use defaults".
                          format(langs=langs[self.tts.lang]))
                raise ValueError

    def validate_connection(self):
        self.tts.get_voice()

    def get_tts_class(self):
        return MbrolaTTS
