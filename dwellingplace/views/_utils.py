from datetime import datetime


TMP_ROOT = "/tmp"  # exists for the duration of a Heroku request


def get_filename(base, ext):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return "{r}/{b}-{t}.{e}".format(r=TMP_ROOT, b=base, t=timestamp, e=ext)
