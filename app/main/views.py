from flask import jsonify, request
from . import main
from ..models import *
from .. import db
import json
from postalcode import *

def to_dict(model_instance, query_instance=None):
    if hasattr(model_instance, '__table'):
    	print "hasattr(model_instance, '__table__')"
        return {c.name: str(getattr(model_instance, c.name)) for c in model_instance.__table__.columns}
    else:
        cols = model_instance.__table__.columns.keys()
        return { cols[i] : getattr(query_instance,cols[i])  for i in range(len(cols)) }

"""@main.route("/userstest")
def getUsersTest():
	userquerylist = User.query.all()
	jsondi = {}
	for i in range(len(userquerylist)):
		di =to_dict(User,userquerylist[i])
		jsondi["user" + str(i+1)] = di
	return json.dumps(jsondi)"""

@main.route("/")
def getUsers():
	return jsonify(server="working")

@main.route('/login', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    postalcode = request.json["postalcode"]
    if User.query.filter_by(username=username).first() is None:
        user = User(username=username, password=password, picture="http://thumbs.dreamstime.com/x/funny-boy-smiling-swimming-googles-9586616.jpg", postal_code=postalcode)
        db.session.add(user)
        db.session.commit()
        locationInfo = getlocationid(postalcode)
        user_id = User.query.filter_by(username=username).first().id
        return jsonify({"result" : True, "location_name" : locationInfo[1], "location_id" : locationInfo[0], "user_id": user_id})
    return jsonify({"result" : False})


@main.route('/games/<int:locationID>/<int:interestID>', methods=["GET"])
def getGames(locationID, interestID):
    games = (Game.query.filter_by(location_id=locationID).filter_by(interest_id=interestID).filter_by(group_id=0).all())
    gamesList = {}
    for i in range(len(games)):
        gamesList["Game" + str(i+1)] = to_dict(model_instance=Game, query_instance=games[i])
    return jsonify(gamesList)


@main.route('/creategame', methods=["POST"])
def createGame():
    userID = request.json["user_id"]
    venueID = request.json["venue_id"]
    locationID = request.json["location_id"]
    interestID = request.json["interest_id"]
    time = request.json["time"]
    maxpax = request.json["max"]
    minpax = request.json["min"]
    num = request.json["num"]
    group_id= request.json["group_id"]
    game = Game(venue_id=venueID, location_id=locationID, time=time, min_players=minpax, max_players=maxpax, interest_id=interestID, num=num, group_id=group_id)
    db.session.add(game)
    db.session.commit()
    game_id = Game.query.filter_by(venue_id=venueID).filter_by(time=time).first().id
    transaction = Transaction(game_id=game_id, user_id=userID, num=num)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"result" : True})


@main.route('/showgame/<int:game_id>', methods=["GET"])
def showGame(game_id):
    game = Game.query.get(game_id)
    game = to_dict(Game, game)
    game["venue_name"] = Venue.query.get(game["venue_id"]).name
    return jsonify(game)

@main.route('/players/<int:gameID>', methods=["GET"])
def getPlayers(gameID):
    players = Transaction.query.filter_by(game_id=gameID).all()
    playersList = {}
    for i in range(len(players)):
        userID = to_dict(Transaction, players[i])["user_id"]
        username = User.query.filter_by(id=userID).first().username
        pictureUrl = to_dict(User, User.query.filter_by(username=username).first())["picture"]
        playersList[i + 1] = { "username":username, "pictureURL":pictureUrl }
    return jsonify(playersList)

@main.route('/venues/<int:locationID>/<int:interestID>', methods=["GET"])
def getVenues(locationID, interestID):
    venues = (Venue.query.filter_by(location_id=locationID).filter_by(interest_id=interestID).all())
    venuesList = {}
    for i in range(len(venues)):
    	currVenue = to_dict(Venue, venues[i])
    	venuesList[currVenue["id"]] = currVenue["name"]
    return jsonify(venuesList)

@main.route('/joingame', methods=["POST"])
def joinGame():
    username = request.json["username"]
    gameID = request.json["game_id"]
    num = request.json["num"]

    #Check if existing transaction entry already exists (user already joined game)
    existingTrans = Transaction.query.filter_by(user_id=User.query.filter_by(username=username).first().id).filter_by(game_id=gameID).first()
    if existingTrans == None:
    	trans = Transaction(game_id=gameID, user_id=User.query.filter_by(username=username).first().id)
    	db.session.add(trans)
    	db.session.commit()
    else:
    	return jsonify({"result" : False})

    game = Game.query.get(gameID)
    newNum = game.num + num
    if newNum > game.max_players:
    	return jsonify({"result" : False})
    else:
    	game.num = newNum
    db.session.commit()
    return jsonify({"result" : True})

@main.route('/groups/<string:userName>', methods=["GET"])
def getGroups(userName):
    userID = User.query.filter_by(username = userName).first().id
    groups = GroupTransaction.query.filter_by(user_id=userID).all()
    print groups
    print "length of groups", len(groups)
    groupList = {}
    for i in range(len(groups)):
        groupID = to_dict(GroupTransaction, groups[i])["group_id"]
        print groupID
        groupList[groupID] = Group.query.get(groupID).name
    return jsonify(groupList)


@main.route('/showgroup/<int:group_id>', methods=["GET"])
def showGroup(group_id):
    group = to_dict(Group, Group.query.get(group_id))
    groupID = group["id"]
    games = (Game.query.filter_by(group_id=groupID).all())
    gamesList = {}
    for i in range(len(games)):
        gamesList["Game" + str(i+1)] = to_dict(Game, games[i])
    return jsonify(gamesList)


@main.route('/creategroup', methods=["POST"])
def createGroup():
    groupname = request.json["group_name"]
    if Group.query.filter_by(name=groupname).first() is None:
		userID = User.query.filter_by(username=request.json["username"]).first().id
		locationID = getlocationid(User.query.get(userID).postal_code)[0]
		group = Group(name=groupname, location_id=locationID)
		db.session.add(group)
		db.session.commit()
		groupID = Group.query.filter_by(name=groupname).first().id
		trans = GroupTransaction(user_id=userID, group_id=groupID)
		db.session.add(trans)
		db.session.commit()
		return jsonify({"result" : True, "group_id" : groupID})
    return jsonify({"result" : False})


@main.route('/addtogroup', methods=["POST"])
def addToGroup():
    userID = User.query.filter_by(username=request.json["username"]).first().id
    groupID = request.json["group_id"]
    if GroupTransaction.query.filter_by(user_id=userID).filter_by(group_id=groupID).first() is None:
		trans = GroupTransaction(group_id=groupID, user_id=userID)
		db.session.add(trans)
		db.session.commit()
		return jsonify({"result" : True})
    return jsonify({"result" : False})




