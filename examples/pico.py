from text2speech.modules.pico_tts import PicoTTS

tts = PicoTTS()
tts.validate()
voices = tts.describe_voices()

tts.get_tts("hello world", "pico.wav")

tts = PicoTTS({"lang": "es-ES"})
tts.get_tts("hola mundo", "pico_es.wav")
