from django.test import TestCase

from stable_diffusion_webui.utils import list_to_matrix


class TestUtils(TestCase):

    def test_list_to_matrix(self):
        items = list(range(10))
        matrix = list_to_matrix(items, 3)
        self.assertEqual(len(matrix), 4)