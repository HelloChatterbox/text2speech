from text2speech.modules.responsive_voice_tts import ResponsiveVoiceTTS


tts = ResponsiveVoiceTTS({"lang": "pt",
                          "voice": "FallbackPortugueseMale"})
tts.validate()

voices = tts.describe_voices()


tts.get_tts("olá mundo", "rv.mp3")

conf = {"lang": "en",
        "gender": "male",
        "pitch": 0.1,
        "rate": 0.25,
        "vol": 1}

slow_joe = ResponsiveVoiceTTS(conf)
slow_joe.run()
slow_joe.execute("My name is jarbas")

