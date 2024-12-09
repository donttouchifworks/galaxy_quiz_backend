from marshmallow import Schema, fields, validates, ValidationError


class RegisterSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required"})
    password = fields.String(required=True, error_messages={"required": "Password is required"})

    @validates("password")
    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must include at least one number")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must include at least one uppercase letter")
        if not any(char in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for char in password):
            raise ValidationError("Password must include at least one special character")


class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required"})
    password = fields.String(required=True, error_messages={"required": "Password is required"})
