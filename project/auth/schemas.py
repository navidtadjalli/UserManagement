from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone_number = fields.Str(
        required=True,
        validate=validate.Regexp(
            regex=r'^((\+|00)98|0)9\d{9}$',
            error='Phone number is invalid.'
        )
    )
    registration_date = fields.DateTime(dump_only=True)
    # blogs = fields.Nested(BlogSchema, many=True)


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
