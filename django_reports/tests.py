import time

from django.core.urlresolvers import reverse
from django.test import TestCase

from django_reports.models import Report


class ReportTest(TestCase):

    def setUp(self):
        # create the main workflow object
        r1 = Report.objects.create(name="Test Report 1", source_code="""
from django_reports.models import Report
from django_reports.highcharts import PieChartReportQuery

class TestQuery1(PieChartReportQuery):
        
    def get_series_data(self, **kwargs):
        return [{"name":r.name, "y":1} for r in Report.objects.all()]
    
    def get_series_name(self, **kwargs):
        return "Reports"
    
    def get_title(self, **kwargs):
        return "Reports"
    
    def get_form(parameter_name):
        pass

query = TestQuery1()
"""
        )

    def test_reports(self):
        r = Report.objects.get(name="Test Report 1")
        r.compile()
        print(r.eval())

    def test_call_view_loads(self):
        response = self.client.get(reverse("report_view"))
        print(response)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("report_view"), data={"get":"values", "report": "Test Report 1"})
        print(response)
        self.assertEqual(response.status_code, 200)

