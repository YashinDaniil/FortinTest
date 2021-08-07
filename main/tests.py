from django.test import TestCase


class MainViewTest(TestCase):
    def test_view_url_history(self):
        response = self.client.get('/v1/history')
        self.assertEqual(response.status_code, 200)

    def test_view_url_clients(self):
        response = self.client.get('/v1/clients')
        self.assertEqual(response.status_code, 200)

    def test_view_url_clients_detail(self):
        response = self.client.get('/v1/clients')
        self.assertEqual(response.status_code, 200)
