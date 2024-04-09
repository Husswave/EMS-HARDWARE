import urequests as requests
import json

class MongoDBHandler:
    def __init__(self, url, api_key):
        self.URL = url
        self.API_KEY = api_key

    def _send_request(self, endpoint, payload):
        headers = {"api-key": self.API_KEY}
        url = self.URL + endpoint
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Error:", response.status_code)
            return None
        return json.loads(response.text)

    def update_device_info(self, device_id, new_energy, new_power):
        try:
            # Define headers and payload for the request
            headers = {"api-key": self.API_KEY}
            update_payload = {
                "dataSource": "AtlasCluster",
                "database": "Raspberry",
                "collection": "Musa",
                "filter": {"deviceID": device_id},
                "update": {"$set": {"cumulativeEnergy": new_energy, "power": new_power}}
            }
            # Send the request
            response = requests.post(self.URL + "updateOne", headers=headers, json=update_payload)
            # Check if the request was successful
            if 200 <= response.status_code < 300:
                print("Device info updated successfully")
            else:
                print("Error: " + str(response.status_code))
            # Close the response
            response.close()
        except Exception as e:
            print(e)

    def get_device_info(self, device_id):
        search_payload = {
            "dataSource": "AtlasCluster",
            "database": "Raspberry",
            "collection": "Musa",
            "filter": {"deviceID": device_id},
        }
        try:
            response_data = self._send_request("findOne", search_payload)
            document = response_data.get('document', {})
            return document.get("tokenBalance"), document.get("state")
        except Exception as e:
            print("Error fetching device info:", e)
            return None, None