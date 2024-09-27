from app import db
from datetime import datetime
import string
import random

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.short_code:
            self.short_code = self.generate_short_code()

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(6))
        
        while URL.query.filter_by(short_code=short_code).first() is not None:
            short_code = ''.join(random.choice(characters) for _ in range(6))
        
        return short_code

    def increment_clicks(self):
        self.clicks += 1
        db.session.commit()

    def __repr__(self):
        return f'<URL {self.id}: {self.original_url} -> {self.short_code}>'
