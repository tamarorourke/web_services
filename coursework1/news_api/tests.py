from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Story
from django.urls import reverse
from django.contrib.auth import SESSION_KEY

# Create your tests here.

class TestAuthor(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", username="test", password="123")

    def test_author(self):
        self.assertEqual(self.author.name, "Test Author")
        self.assertEqual(self.author.username, "test")
        self.assertEqual(self.author.password, "123")

class TestLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.login_url = reverse('login_user')

    def test_successful_login(self):
        response = self.client.post(self.login_url, {'username': "test", 'password': "123"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"message": "Welcome!"})

    def test_unsuccessful_login(self):
        response = self.client.post(self.login_url, {'username': "test", 'password': "wrongpassword"})
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "Invalid login attempt."})

class TestLogout(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')

    def test_logout(self):
        login_response = self.client.post(self.login_url, {'username': "test", 'password': "123"})
        self.assertEqual(login_response.status_code, 200)
        
        # Make sure the user is logged in - check presence of user's ID in the session
        self.assertIn(SESSION_KEY, self.client.session)

        logout_response = self.client.post(self.logout_url)
        
        # Check logout response
        self.assertEqual(logout_response.status_code, 200)
        self.assertJSONEqual(str(logout_response.content, encoding='utf8'), {"message": "Goodbye!"})
        
        # Verify that the session has been cleared
        self.assertNotIn(SESSION_KEY, self.client.session)

class TestStoryPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        
        # Create an Author instance associated with the user
        self.author = Author.objects.create(name="Test Author", username=self.user.username)
        self.client.login(username="test", password="123")

    def test_story_post(self):
        post_story_url = reverse('post_story')

        story_data = {
            'headline': "Test Headline",
            'category': "Test Category",
            'region': "Test Region",
            'details': "Test Details"
        }

        # Post story
        response = self.client.post(post_story_url, story_data, content_type='application/json')
        
        self.assertEqual(response.status_code, 201)

        # Verify the story has been added to the database
        self.assertTrue(Story.objects.filter(headline='Test Headline').exists())

class TestStoryDelete(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="123")
        self.client.login(username="test", password="123")

        self.author = Author.objects.create(name="Test Author", username=self.user.username, password="123")
        
        self.story = Story.objects.create(
            headline="Test Headline",
            category="Test Category",
            region="Test Region",
            author=self.author,
            details="Test Details"
        )

        # URL for deleting story
        self.delete_url = reverse('delete_story', args=[self.story.id])

    def test_successful_story_delete(self):
        # Delete the story
        response = self.client.delete(self.delete_url)

        # Check that the story was deleted successfully
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"message": "Story deleted successfully."})

        # Check that the story no longer exists in the database
        self.assertFalse(Story.objects.filter(id=self.story.id).exists())

    def test_unsuccessful_story_delete(self):
        # Log in as a different user
        self.client.logout()
        another_user = User.objects.create_user(username='anotheruser', password='67890')
        self.client.login(username='anotheruser', password='67890')

        # Try to delete the story which should fail since this user is not the author
        response = self.client.delete(self.delete_url)

        # Check that the deletion was unsuccessful
        self.assertEqual(response.status_code, 404)
        self.assertIn("Story not found or not authorized to delete.", str(response.content))

        # Check that the story still exists in the database
        self.assertTrue(Story.objects.filter(id=self.story.id).exists())


    