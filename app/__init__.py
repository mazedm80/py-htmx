import json

from fastapi.templating import Jinja2Templates

with open("config.json") as config_json:
    config = json.load(config_json)
    users = config["users"]
    secret_key = config["secret_key"]

templates = Jinja2Templates(directory="templates")
