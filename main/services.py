from django.conf import settings
from django.core.cache import cache

from main.models import Subject


def get_cached_subjects_for_student(student_pk):
    if settings.CACHE_ENABLED:
        key = f'subject_list_{student_pk}'
        subject_list = cache.get(key)

        if subject_list is None:
            subject_list = Subject.objects.filter(student__pk=student_pk)
            cache.set(key, subject_list)

    else:
        subject_list = Subject.objects.filter(student__pk=student_pk)

    return subject_list
