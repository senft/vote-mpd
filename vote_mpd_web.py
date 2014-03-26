#!/usr/bin/env python
# encoding: utf-8

from bottle import route, run, template, static_file, post, request, debug

import vote_mpd

mpd = vote_mpd.VoteMPD()


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static/')


@post('/')
@route('/')
def index(song_id=None):
    try:
        song_id = int(request.forms.get('vote'))
        mpd.vote(song_id)
    except TypeError:
        # POST item 'vote' not given
        pass

    return template('index', current_song=mpd.get_current_song(),
                    next_songs=mpd.get_queue(4)[1:],
                    songs=mpd.get_queue()[1:], voted=song_id,
                    remaining_time=(mpd.get_remaining_time() * 1000) + 2)

debug(True)
run(host='0.0.0.0', port=8080)
