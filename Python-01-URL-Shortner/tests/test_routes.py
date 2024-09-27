from tests import TestCase
from app.models import URL
from flask import url_for
import json

class TestRoutes(TestCase):

    def test_index_get(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'URL Shortener', response.data)

    def test_index_post_valid_url(self):
        data = {'url': 'http://example.com'}
        response = self.client.post(url_for('main.index'), data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'URL successfully shortened', response.data)

    def test_index_post_invalid_url(self):
        data = {'url': 'not_a_valid_url'}
        response = self.client.post(url_for('main.index'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid URL', response.data)

    def test_redirect_to_url(self):
        url = self.create_url('http://example.com')
        response = self.client.get(url_for('main.redirect_to_url', short_code=url.short_code))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://example.com')

    def test_url_stats(self):
        url = self.create_url('http://example.com')
        response = self.client.get(url_for('main.url_stats', short_code=url.short_code))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'URL Details', response.data)
        self.assertIn(b'http://example.com', response.data)

    def test_url_stats_not_found(self):
        response = self.client.get(url_for('main.url_stats', short_code='notfound'))
        self.assertEqual(response.status_code, 404)

    def test_increment_clicks(self):
        url = self.create_url('http://example.com')
        initial_clicks = url.clicks
        self.client.get(url_for('main.redirect_to_url', short_code=url.short_code))
        updated_url = URL.query.get(url.id)
        self.assertEqual(updated_url.clicks, initial_clicks + 1)

    def test_recent_urls(self):
        # Create multiple URLs
        urls = [self.create_url(f'http://example{i}.com') for i in range(5)]
        
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        
        for url in urls:
            self.assertIn(url.original_url.encode(), response.data)
            self.assertIn(url.short_code.encode(), response.data)

    def test_api_shorten_url(self):
        data = {'url': 'http://example.com'}
        response = self.client.post(url_for('main.api_shorten_url'), 
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('short_url', data)
        self.assertIn('original_url', data)

    def test_api_shorten_url_invalid(self):
        data = {'url': 'not_a_valid_url'}
        response = self.client.post(url_for('main.api_shorten_url'), 
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_url_stats(self):
        url = self.create_url('http://example.com')
        response = self.client.get(url_for('main.api_url_stats', short_code=url.short_code))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['original_url'], 'http://example.com')
        self.assertEqual(data['clicks'], 0)

    def test_api_url_stats_not_found(self):
        response = self.client.get(url_for('main.api_url_stats', short_code='notfound'))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
