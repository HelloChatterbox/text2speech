from text2speech .modules.spdsay_tts import SpdSay

tts = SpdSay()
tts.validate()
voices = tts.describe_voices()

try:
    tts.get_tts("hello world", "spd.wav")
except NotImplementedError:
    pass

tts.execute("hello world")