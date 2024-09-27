import os
import sys
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import URL
from config import TestConfig

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def create_url(original_url):
    url = URL(original_url=original_url)
    db.session.add(url)
    db.session.commit()
    return url
