#!/usr/bin/python

import datetime

class collection:

	id = -1
	name = ''
	overview = ''

class genre:

	id = -1
	name = ''

	def __init__(self, next=None):
		self.next = next

class person:

	id = -1
	name = ''

	def __init__(self, next=None):
		self.next = next

class movie:

	id = -1
	name = ''
	overview = ''
	rating = 0.0
	released = datetime.date(1899, 01, 01)
	runtime = 0.0
	collection = None
	genres = None
	cast = None

	def getGenresCSV(self):

		genres = []
		g = self.genres
		while (None != g):
			genres.insert(0, g.name)
			g = g.next
		return ', '.join(genres)

	def getCastCSV(self):

		cast = []
		p = self.cast
		while (None != p):
			cast.insert(0, p.name)
			p = p.next
		return ', '.join(cast)

	def display(self):
		print 'Movie(' + str(self.id) + '): ' + self.name
		print '	Rating: ' + str(self.rating)
		print '	Runtime: ' + str(self.runtime)
		print '	Released: ' + str(self.released)
		print '	Genres: ' + self.getGenresCSV()
		print '	Cast: ' + self.getCastCSV()
		print
		print '	Overview: ' + self.overview
		print
		print '	Collection(' + str(self.collection.id) + '): ' + self.collection.name
		print '		Overview: ' + self.collection.overview
