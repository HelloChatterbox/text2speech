from text2speech.modules.voice_rss import VoiceRSSTTS

tts = VoiceRSSTTS({"lang": "pt-pt",
                   "key": ""})
tts.validate()

voices = tts.describe_voices()

tts.get_tts("olá mundo", "rss.mp3")
