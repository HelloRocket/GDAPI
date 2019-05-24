from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from sys import argv

script, filename = argv

print("We're going to erase {}.".format(filename))

target = open(filename, 'w', encoding="utf-8")
target.truncate()


SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

# Auto-iterate through all files that matches this query
files = DRIVE.files().list(q= "'0B8K5jq5Aw7evLUJXdDBsclg3czA' in parents and trashed=false").execute().get('files', [])
for f in files:
    print(f['name'], f['mimeType'])
    cleanline = f['name'].encode('utf-8', 'ignore')
    cleanline = cleanline.decode('utf-8', 'ignore')
    target.write('name: %s, mime: %s' % ( cleanline, f['mimeType']))
    target.write('\n')

print('Done')
target.close()
