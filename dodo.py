from doit.tools import LongRunning
from lol_match_history.data.make_dataset import get_matches_for_team


def task_make_dataset():

    return {
        "actions": [(get_matches_for_team,)],
        "params": [
            {
                "name": "team_members",
                "short": "s",
                "long": "summoner_name",
                "type": list,
                "default": [],
                "help": "Give a list of summoners with multiple -s flags",
            }
        ],
        "verbosity": 2,
        "doc": "Retrives and saves all common matches for specified players",
    }


def task_pytest():
    return {"actions": ["pytest"], "doc": "runs tests with pytest"}


def task_lint():
    cmd = [
        "black .",
        "pylint --rcfile=setup.cfg **/*.py",
        "flake8",
        "bandit -r --ini setup.cfg",
    ]

    for c in cmd:
        yield {
            "name": c.split()[0],
            "actions": [LongRunning(c)],
            "doc": "runs black formatting and linting",
        }


def task_install():
    return {
        "actions": [LongRunning("pip install -r requirements.txt")],
        "doc": "Install all dependencies",
    }
