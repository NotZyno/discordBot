import datetime as date
from . import colors


def getTime():
    return f"{colors.GRAY}[{date.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]{colors.RESET}"
