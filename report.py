import subprocess
from logging import getLogger, StreamHandler, DEBUG
import json


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


FILENAME = 'test.sarif'

def security_check(username):
    data = run_slither()
    if data:
        save_data(data, username)


def run_slither():
    result = subprocess.run(
        ['slither', 'examples/slither-prop', '--sarif', '-'], stdout=subprocess.PIPE)


    if result.returncode != 0:
        logger.error(result.stderr)
    else:
        data = json.loads(result.stdout)
        return data


def save_data(data, filename: str):

    if not data['success']:
        logger.error(data['error'])
    else:
        with open(f"{filename}", "w", encoding="utf-8") as f:
            json.dump(data['results']['printers'][0], f)

        logger.debug("data saved successfully")


def save_sarif(data, filename: str):

    with open(f"{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f)

    logger.debug("data saved successfully")

data = run_slither()
save_sarif(data, FILENAME)