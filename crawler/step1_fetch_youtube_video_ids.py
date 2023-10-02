import os
from apiclient.discovery import build
from apiclient.errors import HttpError
import pandas as pd
import tqdm
import baker
import dotenv
from dotenv import load_dotenv
import httplib2
import google_auth_httplib2
from google.oauth2 import service_account

load_dotenv()

DEVELOPER_KEY = os.environ['YOUTUBE_API_KEY']
PROXY_IP = os.environ['PROXY_IP']
PROXY_PORT = os.environ['PROXY_PORT']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, PROXY_IP, int(PROXY_PORT)
))

SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive',
'https://www.googleapis.com/auth/youtube'
]
SERVICE_ACCOUNT_FILE = './mapfeed-c2a24-33c6b2de0b75.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

authorized_http = google_auth_httplib2.AuthorizedHttp(credentials, http=http)

def youtube_search(query, pageToken, order):
    print('DEBUG youtube_search() | youtube_search() started')
    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
        http=authorized_http
    )

    print('Searching for %s' % query)

    try:
        print('DEBUG youtube_search() | youtube_search().list() started')
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=50,
            type='video',
            videoDuration='short',
            pageToken=pageToken,
            order='relevance',
        ).execute()
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
        return None, []
    rows = []
    for search_result in search_response.get('items', []):
        rows.append({
            'query' : query,
            'YTID': search_result['id']['videoId'],
            'title': search_result['snippet']['title'],
            'description': search_result['snippet']['description'],
        })

    return search_response.get('nextPageToken', ''), rows

def fetch(query, order, pages=1):
    print('DEBUG fetch() | fetch() started')
    rows = []
    pageToken = None
    for i in tqdm.tqdm(range(pages)):
        try:
            pageToken, rows_for_page = youtube_search(query, pageToken, order)
            rows.extend(rows_for_page)
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    return rows

def download(csv_filename, queries, pages=1):
    print('DEBUG download() | download() started')
    order = 'relevance'
    all_rows = []
    for query in queries:
        rows_for_query = fetch(query, order=order, pages=pages)
        all_rows.extend(rows_for_query)

    pd.DataFrame(all_rows).to_csv(csv_filename, index=False)

def main():

    print('DEBUG main() | main() started')
    noise = [
        'weird engine sound',
        'engine buzzing/farting sound',
        'car engine noise',
        'Engine knocking',
        'Engine bad sound',
        'Engine Whining Noise',
        'engine blown sounds',
        'engine tick sound',
        'engine Clicking Noise',
        'engine rattle noise',
        'engine Ticking Noise'
    ]
    healthy = [
        'healthy engine sound',
        'Sound of a Healthy Engine'
    ]


    download('./data/manifest/noise.csv', queries=noise, pages=1)
    download('./data/manifest/healthy.csv', queries=healthy, pages=4)


if __name__ == '__main__':
    main()
