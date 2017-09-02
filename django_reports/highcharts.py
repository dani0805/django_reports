from abc import ABCMeta, abstractmethod

from django_reports.reports import ReportQuery


class PieChartReportQuery(ReportQuery):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_series_data(self, **kwargs):
        pass

    @abstractmethod
    def get_series_name(self, **kwargs):
        pass

    @abstractmethod
    def get_title(self, **kwargs):
        pass

    def eval(self, **kwargs):
        return {
            "chart": {
                "plotBackgroundColor": None,
                "plotBorderWidth": None,
                "plotShadow": False,
                "type": "pie"
            },
            "tooltip": {
                "pointFormat": "{series.name}: <b>{point.percentage:.1f}%</b>"
            },
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": 'pointer',
                    "dataLabels": {
                        "enabled": True,
                        "format": "<b>{point.name}</b>: {point.percentage:.1f} %",
                        "style": {
                            "color": "black"
                        }
                    }
                }
            },
            "series": [{
                "name": self.get_series_name(**kwargs),
                "colorByPoint": True,
                "data": self.get_series_data(**kwargs)
            }]

        }

class BarChartReportQuery(ReportQuery):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_series(self, **kwargs):
        pass

    @abstractmethod
    def get_x_labels(self, **kwargs):
        pass

    @abstractmethod
    def get_title(self, **kwargs):
        pass

    @abstractmethod
    def get_y_title(self, **kwargs):
        pass

    def eval(self, **kwargs):
        return {
            "chart": {
                "type": "column"
            },
            "title": {
                "text": self.get_title(**kwargs)
            },
            "xAxis": {
                "categories": self.get_x_labels(**kwargs),
            },
            "yAxis": {
                min: 0,
                "title": {
                    "text": self.get_y_title(**kwargs)
                },
                "stackLabels": {
                    "enabled": True,
                    "style": {
                        "fontWeight": "bold",
                        "color2":  "gray"
                    }
                }
            },
            "legend": {
                "align": "right",
                "x": -30,
                "verticalAlign": "top",
                "y": 25,
                "floating": True,
                "backgroundColor": "white",
                "borderColor": "#CCC",
                "borderWidth": 1,
                "shadow": False
            },

            "tooltip": {
                "headerFormat": "<b>{point.x}</b><br/>",
                "pointFormat": "{series.name}: {point.y}<br/>Total: {point.stackTotal}"
            },
            "plotOptions": {
                "column": {
                    "stacking": 'normal',
                    "dataLabels": {
                        "enabled": True,
                        "color": "white"
                    }
                }
            },
            "series": self.get_series(**kwargs)


        }