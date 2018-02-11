#!/usr/bin/python

import sqlite3

class movieDB:

	def __init__(self, filename):
		self.conn = sqlite3.connect(filename)

		self.createMoviesTable()
		self.createPersonsTable()
		self.createMoviePersonsTable()
		self.createGenresTable()
		self.createMovieGenresTable()
		self.createCollectionsTable()
		self.createCollectionMoviesTable()
		self.createFilesTable()
		self.createMovieFilesTable()
		self.createStorageTable()

	def createMoviesTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS movies(
	movieId integer primary key,
	name text,
	overview text,
	rating real,
	runtime real,
	released text
)'''
		c.execute(query)

	def createPersonsTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS persons(
	personId integer primary key,
	name text
)'''
		c.execute(query)

	def createGenresTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS genres(
	movieId integer primary key,
	name text
)'''
		c.execute(query)

	def createMovieGenresTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS movie_genres(
	movieGenreId integer primary key,
	movieId integer references movies (movieId),
	genreId integer references genres (genreId)
)'''
		c.execute(query)

	def createMoviePersonsTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS movie_persons(
	moviePersonId integer primary key autoincrement,
	movieId integer references movies (movieId),
	personId integer references persons (personId)
)'''
		c.execute(query)

	def createCollectionsTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS collections(
	collectionId integer primary key,
	name text,
	overview text,
	custom integer
)'''
		c.execute(query)

	def createCollectionMoviesTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS collection_movies(
	collectionMovieId integer primary key,
	collectionId integer references collections (collectionId),
	movieId integer references movies (movieId)
)'''
		c.execute(query)

	def createFilesTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS files(
	fileId integer primary key,
	filename text,
	notes text
)'''
		c.execute(query)

	def createMovieFilesTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS movie_files(
	movieFileId integer primary key,
	movieId integer references movies (movieId),
	fileId integer references files (fileId)
)'''
		c.execute(query)

	def createStorageTable(self):

		c = self.conn.cursor()
		query = '''
CREATE TABLE IF NOT EXISTS storage(
	storageId integer primary key,
	name text,
	regexpat text
)'''
		c.execute(query)

	def updatePerson(self, person):

		c = self.conn.cursor()
		query = '''
INSERT OR REPLACE INTO
	persons(personId, name)
VALUES
	(?, ?)
'''
		try:
			c.execute(query, (person.id, person.name))
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def checkForMoviePerson(self, movieId, personId):

		c = self.conn.cursor()
		query = '''
SELECT
	COUNT(*)
FROM
	movie_persons
WHERE
	movieId=? AND personId=?
'''

		try:
			c.execute(query, (movieId, personId))
			return c.fetchall()[0][0]
		except sqlite3.Error as e:
			print "An error occurred: ", e.args[0]

	def updateMoviePerson(self, movieId, personId):

		if self.checkForMoviePerson(movieId, personId):
			return

		c = self.conn.cursor()
		query = '''
INSERT INTO
	movie_persons(movieId, personId)
VALUES
	(?, ?)
'''
		try:
			c.execute(query, (movieId, personId))
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def updateCast(self, movie):

		c = movie.cast
		while c:
			self.updatePerson(c)
			self.updateMoviePerson(movie.id, c.id)
			c = c.next

	def checkForCollectionMovie(self, collectionId, movieId):

		c = self.conn.cursor()
		query = '''
SELECT
	COUNT(*)
FROM
	collection_movies
WHERE
	collectionId=? AND movieId=?
'''

		try:
			c.execute(query, (collectionId, movieId))
			return c.fetchall()[0][0]
		except sqlite3.Error as e:
			print "An error occurred: ", e.args[0]

	def updateCollectionMovies(self, collectionId, movieId):

		print 'heya'
		if self.checkForCollectionMovie(collectionId, movieId):
			return

		c = self.conn.cursor()
		query = '''
INSERT INTO
	collection_movies(collectionId, movieId)
VALUES
	(?, ?)
'''
		try:
			c.execute(query, (collectionId, movieId))
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def updateCollection(self, movie):

		if (None == movie.collection):
			return

		collection = movie.collection
		c = self.conn.cursor()
		query = '''
INSERT OR REPLACE INTO
	collections(collectionId, name, overview)
VALUES
	(?, ?, ?)

'''

		try:
			c.execute(query, (collection.id, collection.name, collection.overview))
			self.updateCollectionMovies(collection.id, movie.id)
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def updateMovie(self, movie):

		c = self.conn.cursor()
		query = '''
INSERT OR REPLACE INTO
	movies(movieId, name, overview, rating, runtime, released)
VALUES
	(?, ?, ?, ?, ?, ?)
'''
		try:
			c.execute(query, (movie.id, movie.name, movie.overview, movie.rating, movie.runtime, movie.released))
			self.updateCast(movie)
			self.updateCollection(movie)
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

		self.conn.commit()
