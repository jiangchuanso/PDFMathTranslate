class DeepLXTranslator(BaseTranslator):
    name = "deeplx"
    envs = {
        "DEEPLX_ENDPOINT": "http://localhost:8989/translate",
        "DEEPLX_ACCESS_TOKEN": None,
    }
    lang_map = {"zh": "zh-Hans"}

    def __init__(
        self, lang_in, lang_out, model, envs=None, ignore_cache=False, **kwargs
    ):
        self.set_envs(envs)
        super().__init__(lang_in, lang_out, model, ignore_cache)
        self.endpoint = self.envs["DEEPLX_ENDPOINT"]
        self.session = requests.Session()
        auth_key = self.envs["DEEPLX_ACCESS_TOKEN"]
        if auth_key:
            self.endpoint = f"{self.endpoint}?token={auth_key}"

    def do_translate(self, text):
        response = self.session.post(
            self.endpoint,
            json={
                "from": self.lang_in,
                "to": self.lang_out,
                "text": text,
                "html": False,
            },
            verify=False,
        )
        response.raise_for_status()
        return response.json()["data"]
