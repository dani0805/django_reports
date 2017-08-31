import json

from abc import abstractmethod, ABCMeta
from django.core import serializers
from django.views.generic.base import View

from django_reports.models import Report


class ReportQuery:
    """
    Abstract class that must be overridden for every report. Each report must implement ``eval`` and ``get_from``. 
    ``eval`` must provide the input for highcharts as python dictionary. ``get_from`` must provide the name and 
    configurations for each parameter including the choices
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, **kwargs):
        pass

    def _eval(self, **kwargs):
        objects = self.eval(**kwargs)
        return serializers.serialize('json',objects)

    @abstractmethod
    def get_form(self, **kwargs):
        pass

    def _get_form(self, **kwargs):
        objects = self.get_form(**kwargs)
        return serializers.serialize('json',objects)


class ReportView(View):

    def get(self,request):
        if "report" in request.GET and "get" in request.GET :
            report = Report.objects.get(name=request.GET["report"])
            report.compile()
            params = json.loads(request.GET["parameters"]) if "parameters" in request.GET else dict()
            if request.GET["get"] == "form":
                return report.get_form(**params)
            elif request.GET["get"] == "values":
                return report.eval(**params)
        else:
            return serializers.serialize('json', Report.objects.all().values('name', flat=True))