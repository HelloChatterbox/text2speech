from text2speech.modules.mimic2_tts import Mimic2

tts = Mimic2()
tts.validate()
voices = tts.describe_voices()

tts.get_tts("hello world", "kusal.wav")
