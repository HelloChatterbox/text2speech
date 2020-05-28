
class TTSFactory:
    from text2speech.modules.espeak_tts import ESpeak
    from text2speech.modules.espeakng_tts import ESpeakNG
    from text2speech.modules.google_tts import GoogleTTS
    from text2speech.modules.mary_tts import MaryTTS
    from text2speech.modules.mimic_tts import Mimic
    from text2speech.modules.spdsay_tts import SpdSay
    from text2speech.modules.ibm_tts import WatsonTTS
    from text2speech.modules.responsive_voice_tts import ResponsiveVoice
    from text2speech.modules.mimic2_tts import Mimic2
    from text2speech.modules.pico_tts import PicoTTS
    from text2speech.modules.polly_tts import PollyTTS
    from text2speech.modules.festival_tts import FestivalTTS
    from text2speech.modules.voice_rss import VoiceRSSTTS

    CLASSES = {
        "mimic": Mimic,
        "mimic2": Mimic2,
        "google": GoogleTTS,
        "marytts": MaryTTS,
        "espeak": ESpeak,
        "espeak-ng": ESpeakNG,
        "spdsay": SpdSay,
        "watson": WatsonTTS,
        "responsive_voice": ResponsiveVoice,
        "polly": PollyTTS,
        "pico": PicoTTS,
        "festival": FestivalTTS,
        "voicerss": VoiceRSSTTS
    }

    @staticmethod
    def create(tts_config=None):
        """
        Factory method to create a TTS engine based on configuration.

        The configuration file ``chatterbox.conf`` contains a ``tts`` section with
        the name of a TTS module to be read by this method.

        "tts": {
            "module": <engine_name>
        }
        """
        tts_config = tts_config or {}
        tts_module = tts_config.get("module", "google")
        tts_config = tts_config.get(tts_module, {}) or\
                     tts_config.get('tts', {}).get(tts_module, {})
        clazz = TTSFactory.CLASSES.get(tts_module)
        tts = clazz(tts_config)
        tts.validate()
        return tts



