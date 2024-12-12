from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import get_user_model

class UserListViewTest(TestCase):
    def setUp(self):

        self.User = get_user_model()

        self.client = Client()
        self.user1 = self.User.objects.create_user(
            username='alice', first_name='Alice', email='alice@example.com', password='password123'
        )
        self.user2 = self.User.objects.create_user(
            username='bob', first_name='Bob', email='bob@example.com', password='password123'
        )
        self.user3 = self.User.objects.create_user(
            username='charlie', first_name='Charlie', email='charlie@example.com', password='password123'
        )

    def test_template_used(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_retrieve_all_users(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['users'],
            self.User.objects.all(),
            transform=lambda x: x
        )

    def test_filter_users_by_query(self):
        response = self.client.get(reverse('user_list'), {'q': 'alice'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['users'],
            self.User.objects.filter(Q(username__icontains='alice')),
            transform=lambda x: x
        )

        response = self.client.get(reverse('user_list'), {'q': 'Bob'})
        self.assertQuerySetEqual(
            response.context['users'],
            self.User.objects.filter(Q(first_name__icontains='Bob')),
            transform=lambda x: x
        )
        response = self.client.get(reverse('user_list'), {'q': 'example.com'})
        self.assertQuerySetEqual(
            response.context['users'],
            self.User.objects.filter(Q(email__icontains='example.com')),
            transform=lambda x: x
        )

    def test_empty_query_results(self):
        response = self.client.get(reverse('user_list'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['users'],
            self.User.objects.filter(Q(username__icontains='nonexistent') |
                                     Q(first_name__icontains='nonexistent') |
                                     Q(email__icontains='nonexistent')),
            transform=lambda x: x
        )