#!/usr/bin/env python
# encoding: utf-8

from bottle import route, run, template

import vote-mpd


@route('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
