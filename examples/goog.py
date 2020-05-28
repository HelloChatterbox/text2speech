from text2speech.modules.google_tts import GoogleTTS

tts = GoogleTTS()
tts.validate()
voices = tts.describe_voices()

tts = GoogleTTS()
tts.get_tts("hello world", "goog.mp3")

tts = GoogleTTS({"lang": "pt"})
tts.get_tts("olá mundo", "ptgoog.mp3")