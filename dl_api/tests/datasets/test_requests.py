from django.test import TestCase
from .. import tools

class CatsAndDogsTests(TestCase):
    def setUp(self):
        tools.setUpCatsAndDogsDatasetTest(self)

    def test_DatasetCreate(self):
        response = self.client.post(f'/datasets/create', data={
            'name': self.dataset_name,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('name'), self.dataset_name)
        self.assertIsInstance(response.json().get('public_id'), str)

        create_time_str = response.json().get('create_time')
        self.assertIsInstance(create_time_str, str)
        self.assertTrue(tools.dateIsToday(create_time_str))

        self.dataset_public_id = response.json().get('public_id')

    def test_DatasetGet(self):
        # create dataset
        self.test_DatasetCreate()

        # get dataset
        response = self.client.get(f'/datasets/get/{self.dataset_public_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('name'), self.dataset_name)
        self.assertEqual(response.json().get('public_id'), self.dataset_public_id)
        self.assertIsInstance(response.json().get('classes'), dict)

        create_time_str = response.json().get('create_time')
        self.assertIsInstance(create_time_str, str)
        self.assertTrue(tools.dateIsToday(create_time_str))

        last_modified_str = response.json().get('last_modified')
        self.assertIsInstance(last_modified_str, str)
        self.assertTrue(tools.dateIsToday(last_modified_str))
