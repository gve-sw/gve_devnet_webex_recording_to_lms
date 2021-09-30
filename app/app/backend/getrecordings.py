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

import json
import requests
import urllib
import os
import csv
import pandas as pd

from .env import *

# Get recordings from Webex API
def get_recordings(from_date, to_date):
    WEBEX_API = "https://webexapis.com/v1"

    WEBEX_SESSION = requests.Session()
    WEBEX_SESSION.headers.update({
        'Authorization': f"Bearer {WEBEX_TOKEN}"
    })

    url = f"{WEBEX_API}/recordings?from={urllib.parse.quote_plus(from_date)}&to={urllib.parse.quote_plus(to_date)}&siteUrl=cisco.webex.com&max=100"

    RECORDINGS = []
    resp = WEBEX_SESSION.get(url)
    RECORDINGS += resp.json()['items']
    while len(resp.json()['items']) == 100: 
        print("Getting next recordings")
        url = resp.links['next']['url']
        resp = WEBEX_SESSION.get(url)
        RECORDINGS += resp.json()['items']

    recordings = []
    for rec in RECORDINGS:
        entry = {
            "title" : rec["topic"],
            "url" : rec["playbackUrl"],
            "password" : rec["password"]
        }
        recordings += [entry]

    return recordings

# Fetch most recent recordings from Webex API
def get_recent_recordings(from_date, to_date):
    WEBEX_API = "https://webexapis.com/v1"

    WEBEX_SESSION = requests.Session()
    WEBEX_SESSION.headers.update({
        'Authorization': f"Bearer {WEBEX_TOKEN}"
    })

    url = f"{WEBEX_API}/recordings?from={urllib.parse.quote_plus(from_date)}&to={urllib.parse.quote_plus(to_date)}&siteUrl=cisco.webex.com&max=10"

    RECORDINGS = []
    resp = WEBEX_SESSION.get(url)
    RECORDINGS += resp.json()['items']

    recordings = []
    for rec in RECORDINGS:
        entry = {
            "title" : rec["topic"],
            "url" : rec["playbackUrl"],
            "password" : rec["password"]
        }
        recordings += [entry]

    return recordings

# Write recordings to HTML file
def write_recordings(recs, filename):
    with open(filename, "w+") as f:
        # Write preamble
        f.write(
            r"""<html>
                    <head>
                        <style>
                        table {
                        font-family: calibri, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }

                        td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                        }

                        tr:nth-child(even) {
                        background-color: #dddddd;
                        }
                        </style>
                    </head>
                <body>
                
                <h2 style="font-family:verdana">Webex recordings</h2>
                <table>
                <tr>
                    <th>Title</th>
                    <th>Url</th>
                    <th>Password</th>
                </tr>
                """
        )

        for r in recs:
            f.write(
                r"""
                    <tr>
                    <td>""" + r["title"] + r"""</td>
                    <td><a href=" """ + r["url"] + r""" ">Recording link</a></td>
                    <td>""" + r["password"] + r"""</td>
                    </tr>
                """
            )
        
        f.write(
            r"""</table>    
            </body>
            </html>
            """
        )

# Post to COLE page
def post_html_to_cole(title, raw_data):
    data = {}
    headers = {}
    headers['Authorization'] = 'Bearer ' + COLE_ACCESS_TOKEN

    data["wiki_page[title]"] = title
    data["wiki_page[body]"] = raw_data

    url = COLE_URL + title

    requests.put(url, data=data, headers=headers)

# Get recordings + write to HTML file
def full(filename, from_date, to_date):
    recs = get_recordings(from_date, to_date)
    # Store the original json file
    json_file_path = "/app/static/web/recordings.json"
    with open(json_file_path, 'w') as f:
        json.dump(recs, f)
    # Convert json to html and write to an html file
    print("Amount of recordings:" + str(len(recs)))
    write_recordings(recs, filename)

# Helper function for post_to_cole(ecordings_list, df_modules)
def write_module_to_file(html_file_path, df_recordings, row_module):
    # Start new file
    with open(html_file_path, "w") as f:
    # Write preamble
        f.write(
            r"""<html>
                    <head>
                        <style>
                        table {
                        font-family: calibri, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                        }

                        td, th {
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                        }

                        tr:nth-child(even) {
                        background-color: #dddddd;
                        }
                        </style>
                    </head>
                <body>
                
                <h2 style="font-family:verdana">""" + row_module.module_name + r"""</h2>
                """
        )
        # Filter the module from the recordings
        df_module = df_recordings[df_recordings.title.str.contains(row_module.module_name)]
        # Check if empty or not. If empty, then don't post to COLE
        if df_module.empty:
            return False

        for group in row_module.group_names.split(','):
            df_group = df_module[df_module.title.str.contains(group)]
            df_group = df_group.sort_values(by=["title"], ascending=True)

            # Start of sub table
            f.write(
                r"""
                <h3 style="font-family:verdana">""" + group + r"""</h3>
                <table>
                <tr>
                    <th>Title</th>
                    <th>Url</th>
                    <th>Password</th>
                </tr>
                """
            )

            # Write content of table
            for index, row in df_group.iterrows():
                f.write(
                    r"""
                    <tr>
                        <td>""" + row.title + r"""</td>
                        <td><a href=" """ + row.url + r""" ">Recording link</a></td>
                        <td>""" + row.password + r"""</td>
                    </tr>
                    """
                )
            # End of sub table
            f.write(
            r"""</table>   
            <br/>
            """
            )

        # Close of html page
        f.write(
        r"""   
        </body>
        </html>
        """
        )

        # If successfully created HTML page, then push to COLE
        return True

# Post HTML page to COLE
def post_to_cole(recordings_list, df_modules):
    df_recordings = pd.DataFrame(recordings_list) 

    # Loop through the modules
    for _, row in df_modules.iterrows():
        module_name = row.module_name

        html_file_path = f"/app/static/web/{module_name}.html"

        html_page_created = write_module_to_file(html_file_path=html_file_path, df_recordings=df_recordings, row_module=row)

        if html_page_created:
            post_html_to_cole(module_name, open(html_file_path, "r").read())