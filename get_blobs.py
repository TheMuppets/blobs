from __future__ import print_function

import base64
import hashlib
import json
import os
import sys
try:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, Request, HTTPError

blobs = {}
with open("blobs.txt", "r") as f:
    for line in f.readlines():
        sha, path = line.split()
        blobs[path] = sha

def get(path, sha):
    print("acquiring {}".format(sha))
    req = Request("http://localhost:5000/{}".format(sha))
    data = None
    try:
        response = urlopen(req)
        data = response.read()
    except HTTPError as e:
        if e.code == 404:
            print("Unable to locate {}".format(sha)) 
        else:
            print("{} {}".format(e.code, e.message))
        return
    with open(path, "wb") as f:
        print("writing {}".format(sha))
        f.write(data)

for path, sha in blobs.items():
    if os.path.isfile(path):
        with open(path, "rb") as f:
            current_sha = hashlib.sha256(f.read()).hexdigest()
            if current_sha == sha:
                continue
            else:
                get(path, sha)
    else:
        get(path, sha)

