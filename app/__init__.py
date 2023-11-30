import datetime

from fastapi.templating import Jinja2Templates


def convert_time(v: str):
    # convert the date time into time in am/pm format with +6 hours
    v = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")
    v = v + datetime.timedelta(hours=6)
    return v.strftime("%I:%M %p")


templates = Jinja2Templates(directory="templates")
templates.env.filters["convert_time"] = convert_time
