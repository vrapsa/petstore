import cfg
from helpers.api.petstore.client import PetstoreApi


class Api:

    def __init__(self):
        self.petstore = PetstoreApi(cfg.URL)
