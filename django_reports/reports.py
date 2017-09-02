import json

from abc import abstractmethod, ABCMeta
from django.core import serializers
from django.db import models
from django.http.response import HttpResponse
from django.views.generic.base import View

from django_reports.models import Report


class ReportQuery:
    """
    Abstract class that must be overridden for every report. Each report must implement ``eval`` and ``get_form``. 
    ``eval`` must provide the input for highcharts as python dictionary. ``get_form`` must provide the name and 
    configurations for each parameter including the choices
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, **kwargs):
        pass

    def _eval(self, **kwargs):
        objects = self.eval(**kwargs)
        return objects

    @abstractmethod
    def get_form(self, **kwargs):
        pass

    def _get_form(self, **kwargs):
        objects = self.get_form(**kwargs)
        return objects


class ReportView(View):

    def get(self,request):
        if "report" in request.GET and "get" in request.GET :
            report = Report.objects.get(name=request.GET["report"])
            report.compile()
            params = json.loads(request.GET["parameters"]) if "parameters" in request.GET else dict()
            if request.GET["get"] == "form":
                return render_to_json_response(report.get_form(**params))
            elif request.GET["get"] == "values":
                return render_to_json_response(report.eval(**params))
        else:
            return render_to_json_response(
                [
                    {
                        "name":r.name,
                        "title":r.title,
                        "style":r.style,
                        "description":r.description
                    }
                    for r in
                    Report.objects.all()
                ]
            )


def render_to_json_response(obj, **response_kwargs):
    global data
    if isinstance(obj, models.QuerySet):
        data = serializers.serialize('json', obj)
    else:
        data = json.dumps(obj)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)