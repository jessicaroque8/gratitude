from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import PrimaryKeyConstraint
import datetime as dt

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<Entry %r>' % self.title


# declare entry schema for data serialization and validation
class EntrySchema(ma.ModelSchema):
    class Meta:
        model = Entry
        fields = ("id", "title", "body", "created_at")


entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)
