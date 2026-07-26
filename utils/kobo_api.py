import requests

from config.secrets import KOBOTOOLBOX_URL, API_TOKEN

headers = {
    "Authorization": f"Token {API_TOKEN}"
}


def get_submissions(asset_uid, limit=None):
    """
    Downloads submissions from a KoboToolbox form.
    If limit=1, it downloads only one record.
    If limit is None, it downloads all records.
    """

    all_records = []

    url = f"{KOBOTOOLBOX_URL}/api/v2/assets/{asset_uid}/data/"

    if limit is not None:
        url = f"{url}?limit={limit}"

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            return []

        data = response.json()

        all_records.extend(data.get("results", []))

        if limit is not None:
            break

        url = data.get("next")

    return all_records