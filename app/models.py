from . import db

class Interest(db.Model):
	__tablename__ = 'interests'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	#Backrefs
	games = db.relationship('Game', backref='interest-game')
	#Pretty Printing
	def __repr__(self):
		return '<Interest: %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	postal_code = db.Column(db.Integer)
	#Backrefs
	transactions = db.relationship('Transaction', backref='user-transaction')
	#Pretty Printing
	def __repr__(self):
		return '<User: %r>' % self.name

class Transaction(db.Model):
	__tablename__ = 'transactions'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
	num = db.Column(db.Integer)
	#Pretty Printing
	def __repr__(self):
		return '<user_id: %r, game_id = %r, num = %r>' % (self.user_id, self.game_id, self.num)

class Game(db.Model):
	__tablename__ = 'games'
	id = db.Column(db.Integer, primary_key=True)
	venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
	time = db.Column(db.String(64))
	min_players = db.Column(db.Integer)
	max_players = db.Column(db.Integer)
	interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'))
	num = db.Column(db.Integer)
	#Backrefs
	transactions = db.relationship('Transaction', backref='game-transaction')
	#Pretty printing
	def __repr__(self):
		return '<venue_id: %r, time: %r>' % (self.venue_id, self.time)

class Venue(db.Model):
	__tablename__ = 'venues'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	details = db.Column(db.Text)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
	#Backrefs
	games = db.relationship('Game', backref='venue-game')
	def __repr__(self):
		return '<Venue: %r>' % self.name

class Location(db.Model):
	__tablename__ = 'locations'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	#Backrefs
	venues = db.relationship('Venue', backref='location-venue')
	games = db.relationship('Game', backref='location-game')
	#Pretty Printing
	def __repr__(self):
		return '<Location: %r>' % self.name

