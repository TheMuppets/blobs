from __future__ import print_function

import base64
import hashlib
import json
import sys
try:
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen, Request, HTTPError
    
if not len(sys.argv) >=2:
    print("usage: {} list of files to upload".format(sys.argv[0]))
    sys.exit(1)

for arg in sys.argv[1:]:
    with open(arg, 'rb') as f:
        data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        # see if the file exists so we can skip uploading it

        req = Request('http://localhost:5000/{}'.format(sha256))
        req.get_method = lambda: 'HEAD'
        try:
            response = urlopen(req)
            if response.code == 200:
                print('{} already exists, skipping'.format(arg))
                continue
        except HTTPError as e:
            if e.code != 404:
                print('error: {}'.format(e.reason))
        b64 = base64.b64encode(data).decode('utf-8')

        req = Request("http://localhost:5000/upload")
        req.add_header('Content-Type', 'application/json')

        response = urlopen(req, json.dumps({"blob": b64}).encode('utf-8'))
