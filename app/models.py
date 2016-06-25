from . import db

def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's 
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)

class Interest(db.Model):
	__tablename__ = 'interests'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	#Backrefs
	games = db.relationship('Game', backref='interest-game')
	venues = db.relationship('Venue', backref='interest-venue')
	#Pretty Printing
	def __repr__(self):
		return '<Interest: %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64))
	password = db.Column(db.String(64))
	postal_code = db.Column(db.Integer)
	picture = db.Column(db.String(128))
	#Backrefs
	transactions = db.relationship('Transaction', backref='user-transaction')
	groupTransactions = db.relationship('GroupTransaction', backref='user-groupTransaction')
	#Pretty Printing
	def __repr__(self):
		return '<User: %r>' % self.username
	#Conversion into json format
	@property
	def json(self):
		return to_json(self, User)

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
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
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
	interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'))
	latcoord = db.Column(db.String(64))
	longcoord = db.Column(db.String(64))
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
	groups = db.relationship('Group', backref='location-group')
	#Pretty Printing
	def __repr__(self):
		return '<id: %r, Location: %r>' % (self.id, self.name)

class Group(db.Model):
	__tablename__ = 'groups'
	id = db.Column(db.Integer, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
	name = db.Column(db.String(64))
	#Backrefs
	games = db.relationship('Game', backref='group-game')
	groupTransactions = db.relationship('GroupTransaction', backref='group-groupTransaction')
	#Pretty Printing
	def __repr__(self):
		return '<id: %r, location: %r>' % (self.id, self.location_id)

class GroupTransaction(db.Model):
	__tablename__ = 'grouptransactions'
	id = db.Column(db.Integer, primary_key=True)
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	#Pretty Printing
	def __repr__(self):
		return '<group_id: %r, user_id: %r>' % (self.group_id, self.user_id)

