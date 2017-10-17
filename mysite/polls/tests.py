import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "まだ質問がありません。")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        past_question = create_question("過去の質問", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "過去の質問")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: %s>" % past_question.question_text]
        )

    def test_future_question(self):
        future_question = create_question("未来の質問", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        future_question = create_question("未来の質問", 30)
        past_question = create_question("過去の質問", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "過去の質問")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: %s>" % past_question.question_text]
        )

    def test_two_past_questions(self):
        past_question_1 = create_question("過去の質問（５日前）", -5)
        past_question_2 = create_question("過去の質問（３０日前）", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "過去の質問（５日前）")
        self.assertContains(response, "過去の質問（３０日前）")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ["<Question: %s>" % past_question_1.question_text,
            "<Question: %s>" % past_question_2.question_text,]
        )

class DetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("未来の質問", 30)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question("過去の質問", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "過去の質問")
