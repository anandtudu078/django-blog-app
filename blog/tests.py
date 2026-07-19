from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Post, Comment

class BlogTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a test category
        self.category = Category.objects.create(name='Tech Tips', slug='tech-tips')
        
        # Create a published post
        self.post_published = Post.objects.create(
            title='Learning Python',
            slug='learning-python',
            author=self.user,
            category=self.category,
            content='Python is a wonderful programming language. It is easy to learn and fun to use.',
            status=1 # Published
        )
        
        # Create a draft post
        self.post_draft = Post.objects.create(
            title='Future Draft Spec',
            slug='future-draft-spec',
            author=self.user,
            category=self.category,
            content='This is a secret project definition.',
            status=0 # Draft
        )

    def test_category_model(self):
        self.assertEqual(str(self.category), 'Tech Tips')
        self.assertEqual(self.category.get_absolute_url(), '/category/tech-tips/')

    def test_post_model(self):
        self.assertEqual(str(self.post_published), 'Learning Python')
        self.assertEqual(self.post_published.get_absolute_url(), '/post/learning-python/')
        self.assertEqual(self.post_published.read_time, '1 min read')

    def test_comment_model(self):
        comment = Comment.objects.create(
            post=self.post_published,
            name='Alice',
            email='alice@example.com',
            body='Fascinating tutorial!'
        )
        self.assertEqual(str(comment), f"Comment by Alice on {self.post_published}")

    def test_views_status_codes(self):
        # Test Home Page
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Learning Python')
        self.assertNotContains(response, 'Future Draft Spec') # Drafts shouldn't be in lists

        # Test Detail Page (Published)
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'learning-python'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Learning Python')

        # Test Detail Page (Draft - Should return 404)
        response = self.client.get(reverse('post_detail', kwargs={'slug': 'future-draft-spec'}))
        self.assertEqual(response.status_code, 404)

        # Test Category list Page
        response = self.client.get(reverse('category_posts', kwargs={'slug': 'tech-tips'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Learning Python')

        # Test Search Page
        response = self.client.get(reverse('search_posts') + '?q=Python')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Learning Python')

    def test_comment_submission(self):
        post_url = reverse('post_detail', kwargs={'slug': 'learning-python'})
        data = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'body': 'This is a test comment body.'
        }
        
        # Submitting comment POST request
        response = self.client.post(post_url, data)
        self.assertEqual(response.status_code, 302) # Redirects back to detail page
        
        # Verify comment is created but pending approval (active=False by default)
        comment = Comment.objects.get(name='Bob')
        self.assertEqual(comment.body, 'This is a test comment body.')
        self.assertFalse(comment.active)

    def test_login_view(self):
        login_url = reverse('login')
        # Get login page
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        
        # Post valid credentials
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(login_url, data)
        self.assertRedirects(response, reverse('home'))
        
        # Verify user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        # Log the user in first
        self.client.login(username='testuser', password='password123')
        
        logout_url = reverse('logout')
        response = self.client.get(logout_url)
        self.assertRedirects(response, reverse('home'))
        
        # Verify user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_register_view(self):
        register_url = reverse('register')
        # Get register page
        response = self.client.get(register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        
        # Post registration details
        data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(register_url, data)
        self.assertRedirects(response, reverse('home'))
        
        # Verify user was created and is authenticated
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.username, 'newuser')

