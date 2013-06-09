#!/usr/bin/env python
# encoding: utf-8

from bottle import route, run, template, redirect, static_file, debug

import vote_mpd

mpd = vote_mpd.VoteMPD()


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')


@route('/')
def index(name='World'):
    return template('index', songs=mpd.get_queue())


@route('/vote/<song_id:int>')
def vote(song_id):
    mpd.vote(song_id)
    redirect('/')

debug(True)
run(host='0.0.0.0', port=8080)
