#!/usr/bin/env python
# encoding: utf-8

import time
import threading
import logging
from collections import Counter

import mpd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DELAY = 5


class VoteMPD(threading.Thread):
    def __init__(self, hostname='localhost', port=6600):
        threading.Thread.__init__(self)
        self.client = mpd.MPDClient()
        self.votes = Counter()

        self.client.connect(hostname, port)

        state = self.client.status()

        if state['random'] != '0':
            logger.info('mpd: disabled random mode')
            self.client.random(0)

        if state['state'] != 'play':
            logger.info('mpd: started playback')
            self.client.play()

        self.currently_playing = int(self.client.currentsong()['id'])

        self.start()

    def run(self):
        while(True):
            current_id = int(self.client.currentsong()['id'])

            if current_id != self.currently_playing:
                # Song switched!
                if(current_id in self.votes):
                    self.votes.pop(current_id)
                self.currently_playing = current_id

                self.arrange_playlist()

            next_song = self.get_next_song()
            logger.info('Next song will be: {artist} - {title} '.format(
                artist=next_song['artist'], title=next_song['title']))

            time.sleep(DELAY)

    def get_current_song(self):
        return self.client.currentsong()

    def get_next_song(self):
        self.arrange_playlist()
        return self.client.playlistinfo()[1]

    def get_remaining_time(self):
        elapsed = int(float(self.client.status()['elapsed']))
        length = int(self.client.currentsong()['time'])
        return length - elapsed

    def vote(self, song_id):
        # TODO: maybe switch to pos instead of song_id
        logger.debug("Trying to record a vote for song #{song_id}".format(
            song_id=song_id))

        try:
            song = self.get_song(song_id)
        except ValueError:
            raise

        logger.info('Recorded vote for song {artist} - {title} (id={song_id},'
                    ' pos={pos})'.format(song_id=song_id, pos=song['pos'],
                    artist=song['artist'], title=song['title']))

        self.votes[song_id] += 1

        self.arrange_playlist()

    def get_song(self, song_id):
        for song in self.client.playlistinfo():
            if song['id'] == str(song_id):
                return song
        else:
            logger.debug("Couldn't find song with id {song_id}".format(
                song_id=song_id))
            raise ValueError('ID ({song_id}) not found'.format(
                song_id=song_id))

    def arrange_playlist(self):
        # Move currently playing song to pos 0
        playlist = self.client.playlistinfo()
        current_pos = int(self.client.currentsong()['pos'])
        self.client.move((current_pos, len(playlist)), 0)

        # Move songs which have been voted behind the currently playing song
        for offset, (song_id, num_votes) in enumerate(self.votes.most_common(),
                                                      1):
            playlist = self.client.playlistinfo()
            current_pos = int(self.client.currentsong()['pos'])
            song = self.get_song(song_id)
            self.client.move(song['pos'], current_pos + offset)

    def get_queue(self, num_songs=0):
        playlist = self.client.playlistinfo()
        if num_songs == 0:
            return playlist
        return playlist[:num_songs]

#c = VoteMPD()
#print(c.get_queue(1))

#    def main():
#        from random import randint
#        for _ in range(5):
#            try:
#                vote(self.client, randint(0, len(self.client.playlist())))
#            except ValueError:
#                pass
#
#        arrange_playlist(self.client)
#
#        print('Next 3 songs:')
#        print(get_queue(self.client, 3))
#        print('Next songs:')
#        print(get_queue(self.client))
