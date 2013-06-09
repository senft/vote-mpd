#!/usr/bin/env python
# encoding: utf-8

import logging
from collections import Counter

import mpd

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HOSTNAME = 'localhost'
PORT = 6600

connection = mpd.MPDClient()
votes = Counter()

connection.connect(HOSTNAME, PORT)

state = connection.status()

if state['random'] != '0':
    logger.info('mpd: disabled random mode')
    connection.random(0)

if state['state'] != 'play':
    logger.info('mpd: started playback')
    connection.play()


def vote(con, song_id):
    logger.debug("Trying to record a vote for song #{song_id}".format(
        song_id=song_id))

    playlist = con.playlistinfo()

    if song_id > len(playlist):
        raise ValueError('ID {(song_id)} out of range'.format(song_id))

    try:
        song = get_song(playlist, song_id)
    except ValueError:
        raise

    logger.info('Recorded vote for song {artist} - {title} (id={song_id},'
                ' pos={pos})'.format(song_id=song_id, pos=song['pos'],
                artist=song['artist'], title=song['title']))

    votes[song_id] += 1


def get_song(playlist, song_id):
    for song in playlist:
        if song['id'] == str(song_id):
            return song
    else:
        logger.debug("Couldn't find song with id {song_id}".format(
            song_id=song_id))
        raise ValueError('ID ({song_id}) not found'.format(song_id=song_id))


def arrange_playlist(con):
    for offset, (song_id, num_votes) in enumerate(votes.most_common(), 1):
        playlist = con.playlistinfo()
        current_pos = int(con.currentsong()['pos'])
        song = get_song(playlist, song_id)
        con.move(song['pos'], current_pos + offset)


def get_queue(con, num_songs=999):
    playlist = con.playlistinfo()
    current_pos = int(con.currentsong()['pos'])
    return [song for song in playlist
            if current_pos <= int(song['pos']) < current_pos + num_songs]


def main():
    from random import randint
    for _ in range(5):
        try:
            vote(connection, randint(0, len(connection.playlist())))
        except ValueError:
            pass

    arrange_playlist(connection)

    print('Next 3 songs:')
    print(get_queue(connection, 3))
    print('Next songs:')
    print(get_queue(connection))


if __name__ == '__main__':
    main()
