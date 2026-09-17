from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test_user@skypro.com', password='123qwe')
        self.course = Course.objects.create(title='abc')
        self.lesson = Lesson.objects.create(course=self.course, title='ghi', owner=self.user, video_url='https://youtube.com')
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse('materials:lessons_create')
        data = {'title': 'def', 'owner': self.user.pk, 'course': self.course.pk, 'video_url': 'https://youtube.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'def')

    def test_retrieve_lesson(self):
        url = reverse('materials:lessons_retrieve', args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.lesson.title)

    def test_list_lessons(self):
        url = reverse('materials:lessons_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_lesson(self):
        url = reverse('materials:lessons_update', args=[self.lesson.pk])
        data = {'title': 'opr'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'opr')

    def test_delete_lesson(self):
        url = reverse('materials:lessons_delete', args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_valide_url(self):
        url = reverse('materials:lessons_create')
        data = {'title': 'def', 'owner': self.user.pk, 'course': self.course.pk, 'video_url': 'https://yobe.com'}
        response = self.client.post(url, data, format='json')
        print('\n ошибка при валидации:', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test_user@skypro.com', password='123qwe')
        self.course = Course.objects.create(title='abc', owner=self.user)
        self.course_2 = Course.objects.create(title='def', owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription_error(self):
        url = reverse('materials:subscription_create', kwargs={'course_id': self.course.pk})
        data = {'user': self.user.pk, 'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Subscription.objects.all().count(), 1)

    def test_create_subscription(self):
        url = reverse('materials:subscription_create', kwargs={'course_id': self.course_2.pk})
        data = {'user': self.user.pk, 'course': self.course_2.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), 2)

    def test_delete_subscription(self):
        url = reverse('materials:subscription_delete', args=[self.subscription.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.all().count(), 0)
