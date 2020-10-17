from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result = db.Column(JSON)

    def __init__(self, url, result):
        self.url = url
        self.result = result

    def __repr__(self):
        return "<id {}>".format(self.id)
