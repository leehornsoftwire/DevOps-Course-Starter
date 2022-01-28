from __future__ import annotations
from dataclasses import dataclass
import dataclasses
from typing import Dict
import requests

BASE_URL = "https://api.trello.com/1"


@dataclass
class TrelloRequest:
    params: Dict
    url: str

    @classmethod
    def new(cls, token: str, key: str) -> None:
        params = {"token": token, "key": key}
        url = BASE_URL
        return cls(params, url)

    def with_url(self, relative: str) -> TrelloRequest:
        return dataclasses.replace(self, url=f"{self.url}/{relative}")

    def with_params(self, extra_params: Dict[str, str]) -> TrelloRequest:
        return dataclasses.replace(self, params={**extra_params, **self.params})

    def get(self) -> requests.Response:
        return self.request("get")

    def post(self) -> requests.Response:
        return self.request("post")

    def delete(self) -> requests.Response:
        return self.request("delete")

    def put(self) -> requests.Response:
        return self.request("put")

    def request(self, method: str) -> requests.Response:
        return requests.request(method, url=self.url, params=self.params)
