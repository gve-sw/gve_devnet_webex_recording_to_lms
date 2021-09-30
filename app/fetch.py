# Copyright (c) 2020 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import requests
import json
import os
import app.main as main_module
import app.backend.getrecordings as rec_module

def notify_admins(recordings):
    s = requests.Session()
    s.headers.update({
        'Authorization': "Bearer " + os.environ['WEBEX_NOTIFIER_TOKEN']
    })

    WEBEX_BASE_URL = "https://webexapis.com"
    url = WEBEX_BASE_URL + "/v1/messages"

    data = {
        "roomId": os.environ["WEBEX_ROOM_ID"],
        "text": """
            Hello my dear creators!

            I'm here to report I did my job, yay! 
            
            These are the last 10 recordings I retrieved:
            
        """ + json.dumps(recordings, indent=2) + """
            
            Have a great day!
        """, 
    }

    resp = s.post(url, json=data)
    resp.raise_for_status()

def run_flow():
    main_module.recordings()
    main_module.post_to_cole()

if __name__ == "__main__":
    run_flow()

    # Get recent recordings:
    fromdate =  os.environ['FROM_DATE']
    todate =  os.environ['TO_DATE']
    recents = rec_module.get_recent_recordings(fromdate, todate)

    notify_admins(recents)