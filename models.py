from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ApiKey(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    key = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )
