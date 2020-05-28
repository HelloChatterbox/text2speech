from text2speech.modules.mimic_tts import Mimic

tts = Mimic()
tts.validate()
voices = tts.describe_voices()

tts = Mimic({"voice": "kal"})
tts.get_tts("hello world", "kal.wav")


tts = Mimic({"voice": "ap"})
tts.get_tts("hello world", "ap.wav")


tts = Mimic({"voice": "slt"})
tts.get_tts("hello world", "slt.wav")
