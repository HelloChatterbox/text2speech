from text2speech.modules.mary_tts import MaryTTS
from pprint import pprint


tts = MaryTTS()
tts.validate()
tts.get_tts("my name is jarbas", "mary.wav")

voices = tts.describe_voices()
pprint(voices)
