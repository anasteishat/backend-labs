from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    password = fields.Str(required=True, load_only=True)
    

class UserCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100)) 