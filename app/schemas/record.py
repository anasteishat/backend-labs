from marshmallow import Schema, fields, validate
from datetime import datetime

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    datetime = fields.DateTime(dump_only=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))

class RecordCreateSchema(Schema):
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0)) 