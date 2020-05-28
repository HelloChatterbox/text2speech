from text2speech.modules.ibm_tts import WatsonTTS

location = "eu-gb"
instance_id = "xxx2"
url = "https://api.{location}.text-to-speech.watson.cloud.ibm.com/instances/{instance_id}".format(location=location, instance_id=instance_id)

conf = {"lang": "pt",
        "url": url,
        "apikey": ""}

tts = WatsonTTS(conf)
tts.validate()
voices = tts.describe_voices()

tts.get_tts("Olá mundo, o meu nome é Jarbas", "watson.mp3")
