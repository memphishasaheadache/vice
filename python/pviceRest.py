#!/usr/bin/python

import argparse
import glob
import json
import os
import sqlite3

import pmovie
import psql

from flask import Flask
from flask import request

from tmdb3 import Collection, Movie, Person
from tmdb3 import searchMovie
from tmdb3 import set_cache
from tmdb3 import set_key

dbFilename = '/home/memp/vice/python/movies.db'

def parseArguments():

	p = argparse.ArgumentParser(description='Movie data update script')
	p.add_argument('-u', '--update', dest='update', action='store_true')
	p.add_argument('-f', '--file')

	return(p.parse_args())

def getBasename(filename):

	base = os.path.basename(filename)
	base = os.path.splitext(base)[0]
	base = base.replace('_', ' ')
	base = base.replace(':', ' ')
	return base

def getSearchLength(s):

	sLength = len(s)
	if (10 < sLength):
		return 10
	else:
		return sLength

def getMovieJSONStub(filename='[REQUIRED]', movieId='[OPTIONAL]'):

	return(json.dumps(
		[{
			'filename': filename,
			'movieId': movieId
		}],
		indent=2
	))

def invalidMovieJSON(e=None):
	if None == e:
		return "It appears your JSON is invalid, please submit data in the following format:\n" + getMovieJSONStub() + "\n"
	else:
		return "It appears your JSON is invalid, please submit data in the following format:\n" + getMovieJSONStub() + "\n\nError: " + str(e) + "\n"

def searchForMovie(pattern, maxSearch=1):

	s = searchMovie(pattern)

	retBuffer = []
	for i in range(0, maxSearch):
		
		retBuffer.append(s[i])
	return retBuffer

def processMovieUpdate(movie):

	m = movie
	if 'filename' not in m:
		return 'Error: Sadly, filename is a required field\n'

	file = os.path.realpath(m['filename'])
	title = getBasename(file)

	if ('movieId' in m):
		result = Movie(m['movieId'])
	else:
		search = searchForMovie(title)
		if (0 == len(search)):
			return 'No results found for "' + title + '"'

		result = search[0]

	movieStruct = getMovieStruct(result)
	if True == db.updateMovie(movieStruct):
		return 'Success importing (' + str(result.id) + ') ' + result.title + '\n'
	else:
		return 'Failed importing (' + str(result.id) + ') ' + result.title + '\n'

def processMovieUpdates(movieJSON):

	retBuffer = ''
	for moviesData in movieJSON:
		for m in moviesData:
			retBuffer = retBuffer + processMovieUpdate(m)
	return retBuffer

def getMovieStruct(d):

	m = pmovie.movie()
	m.id       = d.id
	m.name     = d.title
	m.overview = d.overview
	m.rating   = d.userrating
	m.runtime  = d.runtime
	m.released = d.releasedate

	if (d.collection):
		m.collection          = pmovie.collection()
		m.collection.id       = d.collection.id
		m.collection.name     = d.collection.name
		m.collection.overview = d.collection.overview

	for g in d.genres:
		newGenre      = pmovie.genre(m.genres)
		newGenre.id   = g.id
		newGenre.name = g.name
		m.genres      = newGenre

	for p in d.cast[:10]:
		newPerson      = pmovie.person(m.cast)
		newPerson.id   = p.id
		newPerson.name = p.name
		m.cast         = newPerson

	return m

# Main

args = parseArguments()
db = psql.movieDB(dbFilename)

set_cache(engine='file', filename='/tmp/tmdb.cache')
set_key('f5a1e6218573b468f59d654ebe6269f9')

mFlask = Flask(__name__)
@mFlask.route('/')
def rootEndpoint():
	return 'Pvice root endpoint\n'

@mFlask.route('/search/<pattern>')
def searchEndpoint(pattern):
	return 'Search endpoint'

@mFlask.route('/movieSearch/<movie>')
def movieSearchEndpoint(movie):

	search = searchMovie(movie)
	start = 0
	while True:
		if 0 == len(search):
			return "No matches found\n"

		maxSearch = getSearchLength(search[start:]) + start

		retBuffer = ''
		for i in range(start, maxSearch):
			retBuffer = retBuffer + str(search[i].id) + '. ' + search[i].title + "\n"

		return retBuffer

@mFlask.route('/update', methods=['POST', 'GET'])
def movieUpdateEndpoint():

	jData = [] 
	if 'POST' == request.method:
		submittedData = request.form.keys()
		for s in submittedData:
			try:
				jData.append(json.loads(s))
					
			except ValueError as e:
				return invalidMovieJSON(e)
	elif 'GET' == request.method:
		return getMovieJSONStub()

	return processMovieUpdates(jData)

mFlask.run()
