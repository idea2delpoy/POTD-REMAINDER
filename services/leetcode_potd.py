import requests

GRAPHQL_URL = "https://leetcode.com/graphql"

def get_leetcode_potd():
    query = {
        "query": """
        query {
          activeDailyCodingChallengeQuestion {
            date
            link
          }
        }
        """
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.post(GRAPHQL_URL, json=query, headers=headers, timeout=10)
    data = res.json()["data"]["activeDailyCodingChallengeQuestion"]

    return {
        "date": data["date"],
        "url": "https://leetcode.com" + data["link"]
    }
