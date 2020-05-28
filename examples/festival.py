from text2speech.modules.festival_tts import FestivalTTS

tts = FestivalTTS()
tts.validate()
voices = tts.describe_voices()
print(voices)
tts.get_tts("hello world", "fest.wav")
