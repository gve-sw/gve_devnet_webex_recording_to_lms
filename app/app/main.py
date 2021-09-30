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

import os
import requests
import json
from flask import Flask, send_file, request
import pandas as pd
from .backend import getrecordings

app = Flask(__name__)

# Home
@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, "index.html")
    return send_file(index_path)

# Uploaded CSV file
@app.route("/upload-file", methods=["GET","POST"])
def upload_file_function():
    uploaded_file = request.files
    file_dict = uploaded_file.to_dict()
    the_file = file_dict["file"]
    the_file.save("/app/app/backend/meeting_list.csv")
    return json.dumps("File has been uploaded")

# Fetch recordings
@app.route("/get-recordings")
def recordings():
    # FY21
    fromdate =  "2020-07-27T09:30:00"
    todate =  "2021-07-27T09:30:00"

    # FY22
    # fromdate =  "2021-08-01T09:30:00"
    # todate =  "2022-08-01T09:30:00"
    try:
        getrecordings.full("/app/static/web/recordings.html", fromdate, todate)
    except Exception as ex:
        print(ex)
    return json.dumps("ok")

# Notify admins about fetched recordings
def notify_admins(recordings):
    s = requests.Session()
    s.headers.update({
        'Authorization': "Bearer " + os.environ['WEBEX_NOTIFIER_TOKEN']
    })

    WEBEX_BASE_URL = "https://webexapis.com"
    url = WEBEX_BASE_URL + "/v1/messages"

    data = {
        "roomId": os.environ['WEBEX_ROOM_ID'],
        "text": """
            Hello my dear creators! 

            I'm here to report I did my job, yay! These are the last 10 recordings I added:
            
        """ + json.dumps(recordings, indent=2) + """

            To remind you, you can find me at: https://emear-apps-test.cisco.com/cole-recording/ (needs VPN)
            
            Have a great day!
        """, 
    }

    resp = s.post(url, json=data)
    resp.raise_for_status()

# Notification 
def notify():
    fromdate =  "2020-07-27T09:30:00"
    todate =  "2021-07-27T09:30:00"
    recents = getrecordings.get_recent_recordings(fromdate, todate)

    notify_admins(recents)

# Post to COLE
@app.route("/post-to-cole")
def post_to_cole():
    #TODO Note: we should do a getrecordings.full call and we should read in that file

    old_file_path = "app/app/static/recordings_list.json"
    recordings_path = "/app/static/web/recordings.json"
    recordings_list = json.loads(open(recordings_path, "r").read()) 

    # Read in uploaded file
    uploaded_file_path = "/app/app/backend/meeting_list.csv"
    df_modules = pd.read_csv(uploaded_file_path, delimiter=";")

    getrecordings.post_to_cole(recordings_list=recordings_list, df_modules=df_modules)

    notify()

    return json.dumps("ok")

# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

