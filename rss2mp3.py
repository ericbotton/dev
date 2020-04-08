import os
import sys
import requests
import feedparser

def download_url(url):
  print('Download url: ' + str(url))
  local_filename = url.split('/')[-1]
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        # Filter out keep-alive chunks
        f.write(chunk)
        # f.flush()
  return local_filename

def print_usage(args):
  print('usage: rss2mp3.py [count] url')
  print('Error: ' + str(args))

count = -1
if len(sys.argv) < 2:
  print_usage('Too few arguments.')
  exit(1)
else:
  try:
    count = int(sys.argv[-2])
  except ValueError as e:
    print_usage('arg "{}" must be integer.'.format(sys.argv[-2]))
    exit(1)

url_arg = sys.argv[-1]

try:
  rss_filename = download_url(url_arg)
except Exception as e:
  print(str(e))
  exit(404)

parsed_feed = feedparser.parse(rss_filename)
os.remove(rss_filename)

podcast_title = parsed_feed['feed']['title']
try:
  os.mkdir(podcast_title)
except FileExistsError as e:
  pass

mp3_files = []

for episode in parsed_feed.entries:
  mp3_files.append(episode['enclosures'][0]['href'])

if count > 0:
  i = count - 1
else:
  i = len(mp3_files)

while i < count:
  f = download_url(mp3_files[i])
  filename = '{} - {}'.format(str(i + 1), f)
  os.rename(f, os.path.join(podcast_title, filename))
  i = i + 1

# vim: ft=python sw=2 ts=2 et
