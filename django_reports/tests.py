import time
from django.test import TestCase

from django_reports.models import Report


class ReportTest(TestCase):

    def setUp(self):
        # create the main workflow object
        r1 = Report.objects.create(name="Test Report 1", source_code="""
from django_reports.models import Report
from django_reports.reports import ReportQuery

class TestQuery1(ReportQuery):
        
    def eval(self, **kwargs):
        return Report.objects.all()
    
    def get_choices(parameter_name):
        pass

query = TestQuery1()
"""
        )

    def test_reports(self):
        r = Report.objects.get(name="Test Report 1")
        r.compile()
        print(r.eval())
