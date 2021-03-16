import subprocess
from text2speech.modules import TTS, TTSValidator


class ESpeak(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"lang": "en-us", "voice": "m1"}
        super(ESpeak, self).__init__(config, ESpeakValidator(self),
                                     ssml_tags=["speak", "say-as", "voice",
                                                "audio", "prosody", "break",
                                                "emphasis", "sub",
                                                "tts:style", "p", "s", "mark"])

    @property
    def gender(self):
        return self.voice[0]

    def modify_tag(self, tag):
        """Override to modify each supported ssml tag"""
        if "%" in tag:
            if "-" in tag:
                val = tag.split("-")[1].split("%")[0]
                tag = tag.replace("-", "").replace("%", "")
                new_val = int(val) / 100
                tag = tag.replace(val, new_val)
            elif "+" in tag:
                val = tag.split("+")[1].split("%")[0]
                tag = tag.replace("+", "").replace("%", "")
                new_val = int(val) / 100
                tag = tag.replace(val, new_val)
        return tag

    def get_tts(self, sentence, wav_file):
        subprocess.call(
            ['espeak', '-m', "-w", wav_file, '-v', self.lang + '+' +
             self.voice, sentence])

        return wav_file, None

    def describe_voices(self):
        output = subprocess.check_output(["espeak", "--voices"]).decode(
            "utf-8")
        voices = {}
        for v in output.split("\n")[1:]:
            if len(v.split()) < 3:
                continue
            _, lang_code = v.split()[:2]
            voices[lang_code] = ["m1", "m2", "m3", "m4", "m5", "m6", "m7",
                                 "f1", "f2", "f3", "f4", "f5", "croak",
                                 "whisper"]
        return voices


class ESpeakValidator(TTSValidator):
    def __init__(self, tts):
        super(ESpeakValidator, self).__init__(tts)

    def validate_connection(self):
        try:
            subprocess.call(['espeak', '--version'])
        except:
            raise Exception(
                'ESpeak is not installed. Run: sudo apt-get install espeak')

    def get_tts_class(self):
        return ESpeak

