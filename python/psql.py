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
	moviePersonId integer primary key,
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
