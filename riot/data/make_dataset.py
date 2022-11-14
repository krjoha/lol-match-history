from riot import logger
import argparse
import json
import os
import time

from riotwatcher import LolWatcher
from limits import storage, strategies, parse


class RiotClient:
    def __init__(self) -> None:
        self.apikey = os.environ.get("riot_apikey", "no_key_defined")
        self.region = os.environ.get("region", "euw1")
        self.data_path = os.environ.get("data_path")

        self.watcher = LolWatcher(api_key=self.apikey)

        self.memory_storage = storage.MemoryStorage()
        self.moving_window = strategies.MovingWindowRateLimiter(self.memory_storage)
        self.rate_limit_item = parse("50/minute")

    def get_profile(self, summoner_name: str) -> dict:
        logger.info(f"Getting profile for summoner '{summoner_name}'")
        self._check_rate_limit()

        profile = self.watcher.summoner.by_name(self.region, summoner_name)
        self._save_response(f"profile_{summoner_name}.json", profile)

        return profile

    def get_matches(
        self, puuid: str, summoner_name: str, start=0, count=100, queue: int = 440
    ) -> dict:
        logger.info(f"Getting match history for summoner '{summoner_name}'")
        self._check_rate_limit()

        game_ids = self.watcher.match.matchlist_by_puuid(
            self.region, puuid, start, count, queue
        )

        if os.environ.get("log_level") == "DEBUG":
            self._save_response(f"matches_id_{summoner_name}.json", game_ids)

        matches = {"matches": []}

        for i, game_id in enumerate(game_ids):
            if i % 10 == 0:
                logger.info(
                    f"Getting match {i + 1} of {len(game_ids)} for player {summoner_name}"
                )

            match = self._get_match_by_id(game_id, summoner_name)
            matches["matches"].append(match)

        self._save_response(f"matches_{summoner_name}.json", matches)
        return matches

    def _get_match_by_id(self, game_id: str, summoner_name: str) -> dict:
        self._check_rate_limit()
        match = self.watcher.match.by_id(self.region, game_id)

        if os.environ.get("log_level") == "DEBUG":
            self._save_response(f"match_{summoner_name}_{game_id}.json", match)

        return match

    def _save_response(self, file_name: str, response: dict):
        logger.debug(response)
        path = os.path.join(self.data_path, "raw", file_name)

        with open(path, "w") as outfile:
            json.dump(response, outfile)

    def _check_rate_limit(self):
        sleep_counter = 0

        while not self.moving_window.test(self.rate_limit_item, "riot"):
            sleep_counter += 1
            logger.debug("rate limit hit - sleeping 0.5 sec")

            if sleep_counter % 10 == 0:
                logger.info(
                    f"rate limit hit - sleeping {self.moving_window.get_window_stats(self.rate_limit_item)}"
                )
            time.sleep(0.5)

        self.moving_window.hit(self.rate_limit_item, "riot")


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--summoner_names",
        nargs="*",
        type=str,
        default=[],
    )
    args = args_parser.parse_args()

    client = RiotClient()

    for summoner_name in args.summoner_names:
        profile = client.get_profile(summoner_name)
        matches = client.get_matches(profile["puuid"], profile["name"])
        logger.info(
            f"Found {len(matches['matches'])} matches for player '{summoner_name}'"
        )

    logger.info(f"Finished work for {len(args.summoner_names)} summoners")
