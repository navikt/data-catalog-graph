from datetime import datetime
from config import db, ma
from marshmallow import fields, pprint
from sqlalchemy.dialects.postgresql import JSONB

class Node(db.Model):
    __tablename__ = "tbl_node"
    id = db.Column(db.Integer, primary_key=True)
    prop = db.Column(JSONB)
    created = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class NodeSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    id = fields.UUID()
    prop = fields.Str(dump_only=True)
    created = fields.Str()
