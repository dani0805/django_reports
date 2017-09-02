from django.db import models
from django.utils.translation import ugettext_lazy

from django_reports.utils import importCode


class Report(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name=ugettext_lazy("Name"))
    title = models.CharField(max_length=100, verbose_name=ugettext_lazy("Name"))
    description = models.CharField(max_length=500, verbose_name=ugettext_lazy("Name"))
    source_code = models.CharField(max_length=4000, verbose_name=ugettext_lazy("Source Code"))
    style = models.CharField(max_length=10, verbose_name=ugettext_lazy("Name"))

    def __init__(self, *args, **kwargs):
        self.query_module = None
        super(Report, self).__init__(*args, **kwargs)

    def compile(self):
        self.query_module = importCode(self.source_code, "query_module")
        print(self.query_module)

    def eval(self, **kwargs):
        if self.query_module:
            return self.query_module.query._eval(**kwargs)
        else:
            raise RuntimeError("Report must be compiled before evaluation")

    def get_form(self, **kwargs):
        if self.query_module:
            return self.query_module.query._get_form(**kwargs)
        else:
            raise RuntimeError("Report must be compiled before evaluation")
