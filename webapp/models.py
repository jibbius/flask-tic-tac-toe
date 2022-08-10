from dataclasses import dataclass, field
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from webapp.event import Event

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))

    e_added = Event()
    e_updated = Event()

    def __init__(self, name, type):
        self.name = name
        self.type = type

        # Commit to database:
        db.session.add(self)
        db.session.commit()

        # Inform any event listeners:
        self.e_added.post_event(self)

    def __repr__(self):
        return "<Player '{}'>".format(self.name)

    def to_dict(self):
        player_as_dict = {
            "id" : self.id,
            "name" : self.name,
            "type" : self.type,
        }
        return player_as_dict

    @classmethod
    def get_players(cls):
        return cls.query.all()

    @classmethod
    def get_player_by_id(cls, player_id:int):
        this_player = cls.query.get(int(player_id))
        return this_player

    @classmethod
    def update_player_by_id(cls, player_id:int, params):
        updated_player = None
        allowable_params = ('name', 'type')
        if len(allowable_params) <= len(allowable_params | params.keys()):
            did_update = cls.query.filter_by(id=int(player_id)).update(params)

            if did_update:
                db.session.commit()
                updated_player = cls.get_player_by_id(player_id)
                cls.e_added.post_event(updated_player)

        return updated_player


