#!/usr/bin/env python
# encoding: utf-8

import mpd

HOSTNAME = 'localhost'
PORT = 6600


def vote(connection, index):
    pass


def main():
    client = mpd.MPDClient()
    client.connect(HOSTNAME, PORT)

    state = client.status()
    if state['state'] != 'play':
        client.play()

    print(state['random'], type(state['random']))
    if state['random'] != '1':
        client.random(1)

    for song in client.playlistinfo():
        print(song['title'])

if __name__ == '__main__':
    main()
