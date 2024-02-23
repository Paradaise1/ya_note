from unittest import skip
from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note


User = get_user_model()


class TestNotes(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'
    SLUG = 'Тестовый слаг'


    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            slug=cls.SLUG,
            author=cls.author,
        )
    
    @skip(reason='')
    def test_successful_creation(self):
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    @skip(reason='')
    def test_title(self):
        data = (
            (self.note.title, self.TITLE),
            (self.note.text, self.TEXT),
            (self.note.slug, self.SLUG),
        )
        for field, expected_result in data:
            with self.subTest():
                self.assertEqual(field, expected_result)
