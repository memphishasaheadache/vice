#!/usr/bin/python

import argparse
import glob
import json
import os
import sqlite3

import pmovie
import psql

from tmdb3 import Collection, Movie, Person
from tmdb3 import searchMovie
from tmdb3 import set_cache
from tmdb3 import set_key

dbFilename = '/home/memp/python/new/movies.db'

def parseArguments():

	p = argparse.ArgumentParser(description='Movie data update script')
	p.add_argument('-u', '--update', dest='update', action='store_true')
	p.add_argument('-f', '--file')

	return(p.parse_args())

def getBasename(filename):

	base = os.path.basename(filename)
	base = os.path.splitext(base)[0]
	base = base.replace('_', ' ')
	return base

def getSearchLength(s):

	sLength = len(s)
	if (10 < sLength):
		return 10
	else:
		return sLength

def importMovieData(d):

	m = pmovie.movie()
	m.id       = d.id
	m.name     = d.title
	m.overview = d.overview
	m.rating   = d.userrating
	m.runtime  = d.runtime
	m.released = d.releasedate

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
file = args.file
update = args.update

if (True == update):
	print 'Updating all data'

if (None == file):
	quit()

db = psql.movieDB(dbFilename)
file = os.path.realpath(file)
movie = getBasename(file)

set_cache(engine='file', filename='/tmp/tmdb.cache')
set_key('f5a1e6218573b468f59d654ebe6269f9')

search = searchMovie(movie)
start = 0
while True:
	maxSearch = getSearchLength(search[start:]) + start

	for i in range(start, maxSearch):
		print str(i + 1) + '. ' + search[i].title
	print
	choice = raw_input('Choose which movie ([n]ext [q]uit): [' + str(start + 1) + '] ')

	if ('' == choice):
		choice = '1'
	elif ('n' == choice):
		start = maxSearch
	elif ('q' == choice):
		quit()

	if choice.isdigit():
		opt = int(choice) - 1
		try:
			if (search[opt]):
				break
		except IndexError:
			print 'Invalid choice'
			print
			continue
		except:
			print("World broken: ", sys.exc_info()[0])
			raise

print
movie = search[opt]
m = importMovieData(movie)
m.display()

#print '	Genres: ' + ','.join(movie.genres)
