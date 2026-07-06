import json
import urllib.request
import urllib.error


class OnlineRankingClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def submit_score(self, player_name, highest_floor, clear_time=None):
        url = self.base_url + "/submit"

        data = {
            "player_name": player_name,
            "highest_floor": highest_floor,
            "clear_time": clear_time,
        }

        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(data).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=3) as response:
                result = json.loads(response.read().decode("utf-8"))

            return result.get("ok", False)

        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            return False

    def get_floor_ranking(self):
        return self.get_json("/rankings/floor")

    def get_time_ranking(self):
        return self.get_json("/rankings/time")

    def get_json(self, path):
        url = self.base_url + path

        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                return json.loads(response.read().decode("utf-8"))

        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError):
            return []