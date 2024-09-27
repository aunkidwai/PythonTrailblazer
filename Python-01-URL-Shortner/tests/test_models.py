from tests import TestCase
from app.models import URL
from app import db
from sqlalchemy.exc import IntegrityError
import time

class TestURLModel(TestCase):

    def test_create_url(self):
        url = self.create_url('http://example.com')
        self.assertIsNotNone(url.id)
        self.assertEqual(url.original_url, 'http://example.com')
        self.assertIsNotNone(url.short_code)
        self.assertEqual(len(url.short_code), 6)
        self.assertIsNotNone(url.created_at)
        self.assertEqual(url.clicks, 0)

    def test_short_code_unique(self):
        url1 = self.create_url('http://example1.com')
        url2 = self.create_url('http://example2.com')
        self.assertNotEqual(url1.short_code, url2.short_code)

    def test_url_representation(self):
        url = self.create_url('http://example.com')
        expected_repr = f'<URL {url.id}: http://example.com -> {url.short_code}>'
        self.assertEqual(repr(url), expected_repr)

    def test_increment_clicks(self):
        url = self.create_url('http://example.com')
        initial_clicks = url.clicks
        url.increment_clicks()
        self.assertEqual(url.clicks, initial_clicks + 1)

    def test_create_url_without_scheme(self):
        url = self.create_url('example.com')
        self.assertEqual(url.original_url, 'http://example.com')

    def test_create_duplicate_url(self):
        url1 = self.create_url('http://example.com')
        url2 = self.create_url('http://example.com')
        self.assertNotEqual(url1.short_code, url2.short_code)

    def test_url_created_at_auto_set(self):
        before = time.time()
        url = self.create_url('http://example.com')
        after = time.time()
        self.assertTrue(before <= url.created_at.timestamp() <= after)

    def test_short_code_generation(self):
        url = URL(original_url='http://example.com')
        self.assertIsNone(url.short_code)
        db.session.add(url)
        db.session.commit()
        self.assertIsNotNone(url.short_code)
        self.assertEqual(len(url.short_code), 6)

    def test_original_url_required(self):
        with self.assertRaises(IntegrityError):
            url = URL()
            db.session.add(url)
            db.session.commit()

    def test_long_url(self):
        long_url = 'http://example.com/' + 'a' * 2000
        url = self.create_url(long_url)
        self.assertEqual(url.original_url, long_url)

    def test_generate_short_code_collision(self):
        # This test simulates a collision in short_code generation
        class MockURL(URL):
            collision_count = 0
            @classmethod
            def query(cls):
                class MockQuery:
                    @staticmethod
                    def filter_by(short_code):
                        MockURL.collision_count += 1
                        return MockQuery if MockURL.collision_count < 3 else None
                    @staticmethod
                    def first():
                        return 'Collision' if MockURL.collision_count < 3 else None
                return MockQuery()

        url = MockURL(original_url='http://example.com')
        url.generate_short_code()
        self.assertEqual(MockURL.collision_count, 3)

    def test_generate_short_code(self):
        url = URL(original_url='http://example.com')
        short_code = url.generate_short_code()
        self.assertEqual(len(short_code), 6)
        self.assertIsNotNone(URL.query.filter_by(short_code=short_code).first())
