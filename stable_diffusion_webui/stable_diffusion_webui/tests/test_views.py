from django.test import TestCase, Client
import json

from stable_diffusion_webui.views import generate_combinations


class TestViews(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()

    def test_generate_two_combinations(self):
        combs = generate_combinations("hi", ['printmaking', "painting"])
        self.assertEqual(len(combs), 2)
    
    def test_generate_three_combinations(self):
        combs = generate_combinations("hi", ['printmaking', "painting"], ['cartoon', 'pop'])
        print(combs)
        self.assertEqual(len(combs), 4)

    def test_generate_image(self):
        params = {
            "subject": "A girl",
            "medium": [],
            "style": [],
            "artist": [],
            "website": [],
            "resolution": [],
            "color": [],
            "lighting": []
        }
        r = self.client.post("/generate_image/", data=params, content_type="application/json")
        self.assertEqual(r.status_code, 200)



