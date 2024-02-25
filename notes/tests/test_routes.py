from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'
    SLUG = 'note-slug'

    @classmethod
    def setUpTestData(cls):
        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            slug=cls.SLUG,
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_user(self):
        pages = ('notes:home', 'users:login', 'users:logout', 'users:signup')
        for page in pages:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        pages = ('notes:list', 'notes:add', 'notes:success')
        for page in pages:
            with self.subTest(page=page):
                url = reverse(page)
                response = self.not_author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        pages = ('notes:detail', 'notes:edit', 'notes:delete')
        users_expected_statuses = (
            (self.not_author_client, HTTPStatus.NOT_FOUND),
            (self.author_client, HTTPStatus.OK)
        )
        for page in pages:
            for user, expected_status in users_expected_statuses:
                with self.subTest(user=user, expected_status=expected_status):
                    url = reverse(page, kwargs={'slug': self.note.slug})
                    response = user.get(url)
                    self.assertEqual(response.status_code, expected_status)

    def test_redirects(self):
        pages_notes = (
            ('notes:detail', self.note),
            ('notes:edit', self.note),
            ('notes:delete', self.note),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None),
        )
        login_url = reverse('users:login')
        for page, note in pages_notes:
            with self.subTest(page=page, note=note):
                if note is not None:
                    url = reverse(page, kwargs={'slug': note.slug})
                else:
                    url = reverse(page)
                expected_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, expected_url)
