from text2speech.modules.polly_tts import PollyTTS

conf = {"voice": "Matthew",
        "key_id": "",
        "secret_key":  "",
        "region": 'us-east-1'}

e = PollyTTS(conf)
e.validate()
voices = e.describe_voices()
ssml = """<speak>
 This is my original voice, without any modifications. <amazon:effect vocal-tract-length="+15%"> 
 Now, imagine that I am much bigger. </amazon:effect> <amazon:effect vocal-tract-length="-15%"> 
 Or, perhaps you prefer my voice when I'm very small. </amazon:effect> You can also control the 
 timbre of my voice by making minor adjustments. <amazon:effect vocal-tract-length="+10%"> 
 For example, by making me sound just a little bigger. </amazon:effect><amazon:effect 
 vocal-tract-length="-10%"> Or, making me sound only somewhat smaller. </amazon:effect> 
</speak>"""
e.get_tts(ssml, "polly.mp3")
