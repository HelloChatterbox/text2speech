import boto3
from botocore.exceptions import NoCredentialsError
from text2speech.modules import TTS, TTSValidator
import logging
from ovos_utils.log import LOG

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.util.retry').setLevel(logging.CRITICAL)


class PollyTTS(TTS):
    works_offline = False
    audio_ext = "mp3"

    def __init__(self, config=None):
        config = config or {"lang": "en"}
        super(PollyTTS, self).__init__(config, PollyTTSValidator(self),
                                       ssml_tags=["speak", "say-as", "voice",
                                                  "prosody", "break",
                                                  "emphasis", "sub", "lang",
                                                  "phoneme", "w", "whisper",
                                                  "amazon:auto-breaths",
                                                  "p", "s", "amazon:effect",
                                                  "mark"])
        self.key_id = self.config.get("key_id", '') or \
                      self.config.get("access_key_id", '')
        self.key = self.config.get("secret_key", '') or \
                   self.config.get("secret_access_key", '')
        self.region = self.config.get("region", 'us-east-1')
        self.polly = boto3.Session(aws_access_key_id=self.key_id,
                                   aws_secret_access_key=self.key,
                                   region_name=self.region).client('polly')
        self.voice = self.config.get("voice") or \
                     self.describe_voices()[self.lang][0]
        self._voices = None

    def get_tts(self, sentence, wav_file):
        text_type = "text"
        if self.remove_ssml(sentence) != sentence:
            text_type = "ssml"
            sentence = sentence.replace("\whispered", "/amazon:effect") \
                .replace("\\whispered", "/amazon:effect") \
                .replace("whispered", "amazon:effect name=\"whispered\"")
        response = self.polly.synthesize_speech(
            OutputFormat=self.audio_ext,
            Text=sentence,
            TextType=text_type,
            VoiceId=self.voice)

        with open(wav_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        return (wav_file, None)  # No phonemes

    def describe_voices(self):
        voices = {}
        for v in self.polly.describe_voices()["Voices"]:
            lang = v["LanguageCode"].lower()
            if lang not in voices:
                voices[lang] = []
            if lang.split("-")[0] not in voices:
                voices[lang.split("-")[0]] = []
            voices[lang.split("-")[0]].append(v["Name"])
            voices[lang].append(v["Name"])

        return voices


class PollyTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PollyTTSValidator, self).__init__(tts)

    def validate_dependencies(self):
        try:
            from boto3 import Session
        except ImportError:
            raise Exception(
                'PollyTTS dependencies not installed, please run pip install '
                'boto3 ')

    def validate_connection(self):
        try:
            if not self.tts.voice:
                raise Exception("Polly TTS Voice not configured")
            output = self.tts.describe_voices()
        except NoCredentialsError:
            LOG.error('PollyTTS credentials not set')
            raise

    def get_tts_class(self):
        return PollyTTS

