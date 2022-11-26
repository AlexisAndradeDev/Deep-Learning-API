from django.test import TestCase
from .. import tools_for_tests

"""
class CatsAndDogsTests(TestCase):
    def setUp(self):
        tools_for_tests.set_up_cats_and_dogs_dataset_test(self)

    def test_DatasetCreate(self):
        response = self.client.post(f'/datasets/create', data={
            'name': self.dataset_name,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('name'), self.dataset_name)
        self.assertIsInstance(response.json().get('public_id'), str)

        create_time_str = response.json().get('create_time')
        self.assertIsInstance(create_time_str, str)
        self.assertTrue(tools_for_tests.date_is_today(create_time_str))

        # check if dataset folder was created
        self.dataset_public_id = response.json().get('public_id')

        self.assertTrue(tools_for_tests.check_if_dataset_root_dir_exists(self.dataset_public_id))

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
        self.assertTrue(tools_for_tests.date_is_today(create_time_str))

        last_modified_str = response.json().get('last_modified')
        self.assertIsInstance(last_modified_str, str)
        self.assertTrue(tools_for_tests.date_is_today(last_modified_str))

    def test_DatasetDelete(self):
        # create dataset
        self.test_DatasetCreate()

        # delete dataset
        response = self.client.delete(f'/datasets/delete/{self.dataset_public_id}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get('Content-Type'), None) # no content

        # check if dataset root folder was deleted
        self.assertFalse(tools_for_tests.check_if_dataset_root_dir_exists(self.dataset_public_id))
    
    def test_DatasetCreateClass(self):
        # create dataset
        self.test_DatasetCreate()

        # create classes
        for class_name in self.expected_classes:
            response = self.client.post(
                f'/datasets/create-class/{self.dataset_public_id}', 
                data={
                    'class_name': class_name,
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json().get('classes'), dict)
        
        self.assertEqual(
            response.json().get('classes'), 
            {
                'cat': {'sets': {}},
                'dog': {'sets': {}},
            }
        )

    def test_DatasetUploadToClassSet(self):
        # create dataset
        self.test_DatasetCreate()

        # create classes
"""