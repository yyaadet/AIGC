from django.test import TestCase, Client
import json

from stable_diffusion_webui.views import _generate_combinations


class TestViews(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def test_generate_two_combinations(self):
        combs = _generate_combinations("hi", ['printmaking', "painting"])
        self.assertEqual(len(combs), 2)
    
    def test_generate_three_combinations(self):
        combs = _generate_combinations("hi", ['printmaking', "painting"], ['cartoon', 'pop'])
        print(combs)
        self.assertEqual(len(combs), 4)

    def test_generate_image(self):
        params = {
            "subject": "A girl",
            "exclude": "",
            "medium": [],
            "style": [],
            "artist": [],
            "website": [],
            "resolution": [],
            "color": [],
            "lighting": []
        }
        """
        r = self.client.post("/generate_image/", data=params, content_type="application/json")
        self.assertEqual(r.status_code, 200)
        
        data = r.json()
        print(data)
        self.assertIsNotNone(data['id'])
        """

    def test_search(self):
        body = {
            "category": "style",
            "q": "2d",
        }
        resp = self.client.post("/search/", data=body, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        resp_data = resp.json()
        print(resp_data)
        self.assertGreater(len(resp_data['data']), 0)



