from marshmallow import Schema, fields, validate

class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float(required=True, validate=validate.Range(min=0))

class BalanceUpdateSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))

account_schema = AccountSchema()
balance_update_schema = BalanceUpdateSchema() 