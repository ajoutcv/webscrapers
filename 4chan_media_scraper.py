import requests
import json
import re
from bs4 import BeautifulSoup

# the baseline for scanning threads
# https://a.4cdn.org/[board]/thread/[op ID].json
# documentation for threads
# https://github.com/4chan/4chan-API/blob/master/pages/Threads.md

# 40574994 < - use the thread ID

# pick the board you want to check for images/files
board = 'wsg'

# base board we're searching
r = requests.get(f'https://a.4cdn.org/{board}/catalog.json')
r = json.loads(r.text)
# what we're looking for
filters = re.compile(r"cats")

# 'walk' through each thread and pull the number of images from each one
# enumerate not needed as you're not indexing
for i in enumerate(r):
    for thread in i[1]['threads']:
        # get each individual thread
        r = requests.get(f"https://a.4cdn.org/{board}/thread/{thread['no']}.json")
        r = json.loads(r.text)
        try:
            # check the posts in the thread thread posts
            for i in r['posts']:
                # filter out what you don't want
                if re.search(filters,i['sub'].lower()) != None:
                    print(i['sub'])
                    print(f"https://a.4cdn.org/{board}/thread/{thread['no']}.json")
                    # get the images/files from all the posts in the thread
                    for post in enumerate(r['posts']):
                        try:
                            print(f"https://i.4cdn.org/{board}/{post[1]['tim']}{post[1]['ext']}")
                            # chuck this stuff into it's own folder, depending on the subject of the thread -> # TODO:
                            with open(f"{post[1]['filename']}{post[1]['ext']}",'wb') as f:
                                f.write(requests.get(f"https://i.4cdn.org/{board}/{post[1]['tim']}{post[1]['ext']}").content)
                        except KeyError:
                            continue
                else:
                    print(i['sub'])
                    continue
        except KeyError:
            continue

        print('-'*10)
