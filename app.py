from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db.init_app(app)

with app.app_context():
    db.create_all()

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    candidates = db.relationship('Candidate', backref='election')#, lazy=True)
    voters = db.relationship('Voter', backref='election')#, lazy=True)
    ballots = db.relationship('Ballot', backref='election')#, lazy=True)

   def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    name = db.Column(db.String)

class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    email = db.Column(db.String)
    hashed_token = db.Column(db.String)

class Ballot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    # TODO: replace with: hidden_content
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

with app.app_context():
    db.create_all()

# TODO: Methods
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/elections/", methods=["GET"])
def election_index():
    return Election.query.all()

@app.route("/elections/", methods=["POST"])
def election_create():
    data = request.get_json()
    election = Election(name=data.get('name', ''), candidates=data.get('candidates', []), voters=data.get('voters', []))
    db.session.add(election)
    db.session.commit()
    return election.as_dict()

@app.route("/elections/<int:id>", methods=["GET"])
def election_show(id):
    election = db.get_or_404(Election, id)
    return election
