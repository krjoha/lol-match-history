from lol_match_history import logger
import argparse
import os
import json

from lol_match_history.data.riot_client import RiotClient


apikey = os.environ.get("riot_apikey", "no_key_defined")
region = os.environ.get("region", "euw1")
data_path = os.environ.get("data_path")


def get_matches_for_team(team_members: list) -> list:
    _get_all_matches_for_each_team_members(team_members)

    team_matches = _prepare_team_only_matches(data_path)
    path = os.path.join(data_path, "interim", "team_matches.json")

    with open(path, "w") as outfile:
        json.dump(team_matches, outfile, indent=4)

    logger.info(f"Saved {len(team_matches)} team matches in {path}")
    return team_matches


def _get_all_matches_for_each_team_members(team_members: list) -> None:
    
    client = RiotClient(apikey, region, data_path)

    all_matches = []
    for summoner_name in team_members:
        profile = client.get_profile(summoner_name)
        matches = client.get_matches(profile["puuid"], profile["name"])
        logger.info(
            f"Found {len(matches['matches'])} matches for player '{summoner_name}'"
        )
        all_matches.append(matches)

    logger.info(f"Finished getting matches for {len(team_members)} summoners")


def _prepare_team_only_matches(data_path: str) -> dict:
    team_members = _prepare_team_member_info(data_path)

    raw_data_path = os.path.join(data_path, "raw")
    files = os.listdir(raw_data_path)

    match_files = [file for file in files if file.startswith("matches_")]
    team_matches = {}

    for match_file in match_files:
        with open(os.path.join(raw_data_path, match_file)) as f:
            player_matches = json.load(f)["matches"]
            
            for match in player_matches:
                participants = match["metadata"]["participants"]

                if set(participants).issuperset(team_members.keys()):
                    team_matches[match["metadata"]["matchId"]] = match

    return team_matches


def _prepare_team_member_info(data_path: str) -> dict:
    raw_data_path = os.path.join(data_path, "raw")
    files = os.listdir(raw_data_path)

    profile_files = [file for file in files if file.startswith("profile_")]

    team_members = {}

    for profile_file in profile_files:
        with open(os.path.join(raw_data_path, profile_file)) as f:
            profile = json.load(f)
            
            summoner_name = profile["name"]
            player_uuid = profile["puuid"]
            team_members[player_uuid] = summoner_name

    path = os.path.join(data_path, "interim", "team_member_info.json")

    with open(path, "w") as outfile:
        json.dump(team_members, outfile, indent=4)
    
    return team_members


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--team_members",
        nargs="*",
        type=str,
        default=[],
    )
    args = args_parser.parse_args()

    get_matches_for_team(args)    
