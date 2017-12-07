from app import db

# Room model
class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    sharinglink = db.Column(db.String(128), unique=True)
    videoURL = db.Column(db.String(256))
    team1 = db.Column(db.String(64))
    team2 = db.Column(db.String(64))

    def __repr__(self):
        return "Room Link : {}. streaming YouTube video : {}".format(self.sharinglink, self.videoURL)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(64))
