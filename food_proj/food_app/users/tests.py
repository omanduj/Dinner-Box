from django.test import TestCase
from .views import find_one_user, get_one_user, insert_one_user
from .db_operations import add_note, check_note_exists, get_user_notes, delete_note

# Create your tests here.
class RandomTest(TestCase):
    def test_user_found(self):
        real_response = find_one_user('123@gmail.com')
        fake_response = find_one_user('abc@123.com')

        assert real_response == True
        assert fake_response == False
        
    def test_get_user(self):
        real_response = get_one_user('omanduj@gmail.com')
        fake_response = get_one_user('abc@123.com')

        assert real_response != False
        assert fake_response == False

    def test_insert_user(self):
        response = insert_one_user({'email': '12345@gmail.com'})
        assert response == True

    def test_add_note(self):
        response = add_note('bob@123.com', 'bob', 'I love my name', 4)
        assert response == 'Note Added'

    def test_existing_note(self):
        response = add_note('bob@123.com', 'bob', 'I love my name', 4)
        assert check_note_exists('bob@123.com', 'bob') != None
        assert check_note_exists('abc@123.com', 'food') == None

    def test_get_user_notes(self):
        notes = get_user_notes('bob@123.com')
        fake_notes = get_user_notes('123@123.com')
        assert notes != None
