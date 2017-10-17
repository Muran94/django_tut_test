import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice

class QuestionModelTests(TestCase):
    def test_was_published_recently_for_future_question(self):
        future_time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=future_time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_for_recent_question(self):
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=recent_time)
        self.assertEqual(recent_question.was_published_recently(), True)

    def test_was_published_recently_for_past_question(self):
        past_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=past_time)
        self.assertEqual(past_question.was_published_recently(), False)
