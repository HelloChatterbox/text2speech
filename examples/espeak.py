from text2speech.modules.espeak_tts import ESpeak
from text2speech.modules.espeakng_tts import ESpeakNG as ESpeak


tts = ESpeak()
tts.validate()
voices = tts.describe_voices()


tts = ESpeak({"voice": "whisper"})
tts.get_tts("hello world", "whisper.wav")

tts = ESpeak({"voice": "croak"})
tts.get_tts("hello world", "croak.wav")

tts = ESpeak({"voice": "f1"})
tts.get_tts("hello world", "female.wav")

tts = ESpeak({"voice": "m1", "lang": "pt"})
tts.get_tts("olá mundo", "male.wav")

