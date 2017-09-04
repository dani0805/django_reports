==============
Django Reports
==============

This project aim is to provide a simple database driven reporting engine that output json and highcharts formatted data.

----

Highcharts
----------

The module ``highcharts`` has some spcialized classes for highcharts preformatted json output. The following examples
illustrate a bar chart, a group pie chart and a stacked bar chart. More highcharts model will be supported in the future.

Pie Charts
++++++++++
The class ``PieChartReportQuery`` specify 4 abstract methods that need to be implemented:

:get_series_data(self, \*\*kwargs): takes any number of keyword parameters and returns an
    array of data points of the format ``[{"name": "<label>", "y": <value>}``

:get_series_name(self, \*\*kwargs): takes any number of keyword parameters and returns
    and returns a string

:get_title(self, \*\*kwargs): takes any number of keyword parameters and returns and
    returns a string

:get_form(self, \*\*kwargs): takes any number of keyword parameters and returns and returns
    an array of dictionaries that define the filter form for the report. The specific
    format depends on the form standard.

::

    from django_reports.highcharts import PieChartReportQuery
    from my_app.models import Product, Sale, Category
    from django.db.models import Count

    FIELD_NAMES = {
        "Product": "product__id__in",
        "Category": "category__id__in",
    }

    class SalesQuery(PieChartReportQuery):

        def get_series_data(self, **kwargs):
            selected_fields = kwargs.get("selected_fields",{})
            selected_fields = {FIELD_NAMES[f]:selected_fields[f] for f in selected_fields.keys() if len(selected_fields[f]) > 0}
            objects = Sale.objects.all()
            if len(selected_fields.keys()) > 0:
                objects = objects.filter(**selected_fields)
            return [{"name": r['product__name'], "y": r['total']} for r in
                objects.values('product__name').annotate(
                    total=Count('product__name')).order_by('total')]

        def get_series_name(self, **kwargs):
            return "Sales"

        def get_title(self, **kwargs):
            return "Sales"

        def get_form(self, **kwargs):
            return [
                {"title":"Product", "type": "dropdown", "options": [(r.id, r.name) for r in Product.objects.all()], "selected": []},
                {"title":"Category", "type": "dropdown", "options": [(r.id, r.name) for r in Category.objects.all()], "selected": []},
            ]


    query = SalesQuery()

Grouped and Stacked Bar Charts
++++++++++++++++++++++++++++++

``BarChartReportQuery`` implements both stacked and group bar charts. The interfaces is slightly
more complex then for pie charts as this charts support multiple series. The data method requirer therefore an
indentifier that you can then use to select the appropriate data. You also need to provide
``x`` labels and series names. These are the methods that you need to implement:

:get_series_data(self, series, \*\*kwargs): takes the series name and any number of keyword parameters and returns an
    array of data points of the values

:get_series_names(self, \*\*kwargs): takes any number of keyword parameters and returns
    and returns an array of strings

:get_x_labels(self, \*\*kwargs): takes any number of keyword parameters and returns an array of strings

:get_title(self, \*\*kwargs): takes any number of keyword parameters and returns and
    returns a string

:get_form(self, \*\*kwargs): takes any number of keyword parameters and returns and returns
    an array of dictionaries that define the filter form for the report. The specific
    format depends on the form standard.

::

    from django_reports.highcharts import PieChartReportQuery
    from my_app.models import Product, Sale, Category
    from django.db.models import Count

    FIELD_NAMES = {
        "Product": "product__id__in",
        "Category": "category__id__in",
    }

    class SalesQuery(PieChartReportQuery):

        def get_series_names(self, series, **kwargs):
            return Category.object.all().values_list("name",flat=True)

        def get_series_data(self, series, **kwargs):
            selected_fields = kwargs.get("selected_fields",{})
            selected_fields = {FIELD_NAMES[f]:selected_fields[f] for f in selected_fields.keys() if len(selected_fields[f]) > 0}
            objects = Sale.objects.filter(category__name=series)
            if len(selected_fields.keys()) > 0:
                objects = objects.filter(**selected_fields)
            return [r['total']} for r in
                objects.values('product__name').annotate(
                    total=Count('product__name')).order_by('product__name')]

        def get_x_labels(self, **kwargs):
            return Product.objects.all().order_by('name').values_list("name",flat=True)

        def get_series_name(self, **kwargs):
            return "Sales"

        def get_title(self, **kwargs):
            return "Sales"

        def get_form(self, **kwargs):
            return [
                {"title":"Product", "type": "dropdown", "options": [(r.id, r.name) for r in Product.objects.all()], "selected": []},
                {"title":"Category", "type": "dropdown", "options": [(r.id, r.name) for r in Category.objects.all()], "selected": []},
            ]

    query = SalesQuery()
