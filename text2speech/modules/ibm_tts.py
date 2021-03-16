from requests.auth import HTTPBasicAuth
from text2speech.modules import RemoteTTS, TTSValidator


class WatsonTTS(RemoteTTS):
    PARAMS = {'accept': 'audio/wav'}

    def __init__(self, config=None,
                 url=None,
                 api_path='/v1/synthesize'):
        config = config or {"lang": "en-us"}
        super(WatsonTTS, self).__init__(config, url, api_path,
                                        WatsonTTSValidator(self))
        user = self.config.get("user") or self.config.get("username")
        password = self.config.get("password")
        api_key = self.config.get("apikey")
        if self.url.endswith(self.api_path):
            self.url = self.url[:-len(self.api_path)]

        if api_key is None:
            self.auth = HTTPBasicAuth(user, password)
        else:
            self.auth = HTTPBasicAuth("apikey", api_key)
        self._voices = None
        if not self.voice:
            if self.lang.lower() in self.describe_voices():
                self.voice = self.describe_voices()[self.lang.lower()][0]
            elif self.lang.lower().split("-")[0] in self.describe_voices():
                self.voice = self.describe_voices()[self.lang.lower().split("-")[0]][0]

    def build_request_params(self, sentence):
        params = self.PARAMS.copy()
        params['LOCALE'] = self.lang
        params['voice'] = self.voice
        params['text'] = sentence.encode('utf-8')
        params['X-Watson-Learning-Opt-Out'] = self.config.get('X-Watson-Learning-Opt-Out', 'true')
        return params

    def describe_voices(self):
        if self._voices is None:
            data = self.session.get(self.url + "/v1/voices",
                                    auth=self.auth).result().json()
            self._voices = data
        else:
            data = self._voices
        voices = {}
        for voice in data["voices"]:
            lang = voice["language"].lower()
            if lang not in voices:
                voices[lang] = []
            if lang.split("-")[0] not in voices:
                voices[lang.split("-")[0]] = []
            voices[lang].append(voice["name"])
            voices[lang.split("-")[0]].append(voice["name"])
        return voices


class WatsonTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(WatsonTTSValidator, self).__init__(tts)

    def validate_connection(self):
        config = self.tts.config
        user = config.get("user") or config.get("username")
        password = config.get("password")
        apikey = config.get("apikey")
        if user and password or apikey:
            return
        else:
            raise ValueError('user/pass or apikey for IBM tts is not defined')

    def get_tts_class(self):
        return WatsonTTS
