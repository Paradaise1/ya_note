from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestContent(TestCase):
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

    def test_notes_list_for_different_users(self):
        url = reverse('notes:list')
        users_note_in_list = (
            (self.author_client, True),
            (self.not_author_client, False),
        )
        for user, note_in_list in users_note_in_list:
            with self.subTest(user=user, note_in_list=note_in_list):
                response = user.get(url)
                object_list = response.context['object_list']
                self.assertIs((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        pages_kwargs = (
            ('notes:add', None),
            ('notes:edit', {'slug': self.note.slug}),
        )
        for page, kwargs in pages_kwargs:
            with self.subTest(page=page, kwargs=kwargs):
                url = reverse(page, kwargs=kwargs)
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
