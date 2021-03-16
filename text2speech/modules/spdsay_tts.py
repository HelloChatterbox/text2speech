import subprocess

from text2speech.modules import TTS, TTSValidator


class SpdSay(TTS):
    def __init__(self, config=None):
        config = config or {"lang": "en-us"}
        # TODO rate pitch volume ssml
        super(SpdSay, self).__init__(config, SpdSayValidator(self))
        self.voice = self.describe_voices()[self.lang][0]

    def execute(self, sentence, ident=None):
        self.begin_audio()
        subprocess.call(
            ['spd-say', '-l', self.lang, '-t', self.voice, sentence])
        self.end_audio()

    def describe_voices(self):
        out = subprocess.check_output(["spd-say", "-L"]).decode(
            "utf-8").split("\n")
        voices = {}
        for line in out[1:]:
            if len(line.split()) < 3:
                continue
            name, code, variant = line.split()
            if variant != "none":
                voices[code + "-" + variant] = [name]
            else:
                voices[code] = [name]
        return voices


class SpdSayValidator(TTSValidator):
    def __init__(self, tts):
        super(SpdSayValidator, self).__init__(tts)

    def validate_connection(self):
        try:
            subprocess.call(['spd-say', '--version'])
        except:
            raise Exception(
                'SpdSay is not installed. Run: sudo apt-get install '
                'speech-dispatcher')

    def get_tts_class(self):
        return SpdSay
