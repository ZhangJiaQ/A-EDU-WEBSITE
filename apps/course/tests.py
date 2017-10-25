from django.test import TestCase
from apps.course.models import Course


class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name='one')

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Course.objects.get(name="one")
        self.assertEqual(lion.__str__(), 'ne')