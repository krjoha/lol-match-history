from lol_match_history import logger
import json
import os
import time

from riotwatcher import LolWatcher
from limits import storage, strategies, parse


class RiotClient:
    def __init__(self, apikey: str, region: str, data_path: str) -> None:
        self.region = region
        self.data_path = data_path
        self.watcher = LolWatcher(api_key=apikey)

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
                    f"Getting match {i+1} of {len(game_ids)} for player {summoner_name}"
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
                    f"rate limit hit - sleeping for {self.moving_window.get_window_stats(self.rate_limit_item)[1]-(sleep_counter*0.5)}"
                )
            time.sleep(0.5)

        self.moving_window.hit(self.rate_limit_item, "riot")
