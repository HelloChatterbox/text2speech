import subprocess
from text2speech.visimes import VISIMES
from text2speech.modules import TTS, TTSValidator
from ovos_utils.log import LOG
import distutils.spawn


class Mimic(TTS):
    audio_ext = "wav"

    def __init__(self, config=None):
        config = config or {"voice": "ap", "lang": "en-us",  "bin": None}
        if not config.get("bin"):
            config["bin"] = distutils.spawn.find_executable("mimic")
        super(Mimic, self).__init__(config, MimicValidator(self),
            ssml_tags=["speak", "ssml", "phoneme", "voice", "audio", "prosody"]
        )
        self.clear_cache()

    def modify_tag(self, tag):
        for key, value in [
            ('x-slow', '0.4'),
            ('slow', '0.7'),
            ('medium', '1.0'),
            ('high', '1.3'),
            ('x-high', '1.6'),
            ('speed', 'rate')
        ]:
            tag = tag.replace(key, value)
        return tag

    @property
    def MIMIC_BIN(self):
        return self.config["bin"]

    @property
    def args(self):
        """ Build mimic arguments. """
        args = [self.MIMIC_BIN, '-voice', self.voice, '-psdur', '-ssml']

        stretch = self.config.get('duration_stretch', None)
        if stretch:
            args += ['--setf', 'duration_stretch=' + stretch]
        return args

    def get_tts(self, sentence, wav_file):
        #  Generate WAV and phonemes
        phonemes = subprocess.check_output(self.args + ['-o', wav_file,
                                                        '-t', sentence])
        return wav_file, phonemes.decode()

    def visime(self, output):
        visimes = []
        pairs = str(output).split(" ")
        for pair in pairs:
            pho_dur = pair.split(":")  # phoneme:duration
            if len(pho_dur) == 2:
                visimes.append((VISIMES.get(pho_dur[0], '4'),
                                float(pho_dur[1])))
        return visimes

    def describe_voices(self):
        #  Generate WAV and phonemes
        out = subprocess.check_output([self.MIMIC_BIN, "-lv"]).decode(
            "utf-8")
        voices = {self.lang: out.split()[2:]}
        return voices


class MimicValidator(TTSValidator):
    def __init__(self, tts):
        super(MimicValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO: Verify version of mimic can handle the requested language
        assert self.tts.lang.split("-")[0].lower() == "en"

    def validate_connection(self):
        try:
            subprocess.call([self.tts.MIMIC_BIN, '--version'])
        except:
            LOG.info("Failed to find mimic binary")
            raise Exception(
                'Mimic was not found. See https://forslund.github.io/mycroft-desktop-repo/')

    def get_tts_class(self):
        return Mimic
