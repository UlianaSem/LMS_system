import json

from django.core.management import BaseCommand
from main.models import Student


class Command(BaseCommand):

    PATH = 'new_student_data.json'

    def handle(self, *args, **options):
        students = self.open_file__()
        students_for_create = []

        for student in students:
            students_for_create.append(Student(**student))

        Student.objects.bulk_create(students_for_create)

    @classmethod
    def open_file__(cls):
        with open(cls.PATH, 'r', encoding='utf-8') as file:
            data_for_open = file.read()

        json_data = json.loads(data_for_open)

        return json_data
