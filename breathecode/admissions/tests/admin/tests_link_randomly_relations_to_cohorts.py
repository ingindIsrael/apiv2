"""
Test /cohort/user
"""
from unittest.mock import patch
from breathecode.tests.mocks.django_contrib import DJANGO_CONTRIB_PATH, apply_django_contrib_messages_mock
from breathecode.admissions.models import Cohort
from breathecode.admissions.admin import link_randomly_relations_to_cohorts
from ..mixins import AdmissionsTestCase
from django.http.request import HttpRequest


class CohortUserTestSuite(AdmissionsTestCase):
    """Test /cohort/user"""
    """
    🔽🔽🔽 With zero Cohort
    """
    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    def test_link_randomly_relations_to_cohorts__with_zero_cohorts(self):
        request = HttpRequest()
        queryset = Cohort.objects.all()

        link_randomly_relations_to_cohorts(None, request, queryset)

        self.assertEqual(self.all_cohort_dict(), [])

    """
    🔽🔽🔽 With one Cohort
    """

    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    def test_link_randomly_relations_to_cohorts__with_one_cohort(self):
        # self.generate_models(academy=True, skip_cohort=True)
        model = self.generate_models(academy=True, cohort=True)

        request = HttpRequest()
        queryset = Cohort.objects.all()

        link_randomly_relations_to_cohorts(None, request, queryset)
        self.assertEqual(self.all_cohort_dict(), [{**self.model_to_dict(model, 'cohort')}])

    """
    🔽🔽🔽 With one Cohort and SyllabusVersion
    """

    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    def test_link_randomly_relations_to_cohorts__with_one_cohort__with_syllabus_version(self):
        # self.generate_models(academy=True, skip_cohort=True)
        cohort_kwargs = {'syllabus_version': None}
        model = self.generate_models(academy=True,
                                     cohort=True,
                                     syllabus=True,
                                     syllabus_version=True,
                                     cohort_kwargs=cohort_kwargs)

        request = HttpRequest()
        queryset = Cohort.objects.all()

        link_randomly_relations_to_cohorts(None, request, queryset)
        self.assertEqual(self.all_cohort_dict(),
                         [{
                             **self.model_to_dict(model, 'cohort'),
                             'syllabus_version_id': 1,
                         }])

    """
    🔽🔽🔽 With one Cohort, SyllabusVersion and SpecialtyMode
    """

    @patch(DJANGO_CONTRIB_PATH['messages'], apply_django_contrib_messages_mock())
    def test_link_randomly_relations_to_cohorts__with_one_cohort__with_specialty_mode(self):
        # self.generate_models(academy=True, skip_cohort=True)
        cohort_kwargs = {'syllabus_version': None, 'specialty_mode': None}
        model = self.generate_models(academy=True,
                                     cohort=True,
                                     syllabus=True,
                                     syllabus_version=True,
                                     specialty_mode=True,
                                     cohort_kwargs=cohort_kwargs)

        request = HttpRequest()
        queryset = Cohort.objects.all()

        link_randomly_relations_to_cohorts(None, request, queryset)
        self.assertEqual(self.all_cohort_dict(),
                         [{
                             **self.model_to_dict(model, 'cohort'),
                             'syllabus_version_id': 1,
                             'specialty_mode_id': 1,
                         }])
