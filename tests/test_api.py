# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from .utils import load


def describe_metrics():

    def describe_GET():

        def it_returns_all_metrics(client, metric):
            status, content = load(client.get("/api/metrics/"))

            expect(status) == 200
            expect(content) == [
                {
                    'PropertyID': "id1",
                    'Date': "Sat, 05 Nov 2016 00:00:00 GMT",
                    'extra': 42,
                },
            ]


def describe_metrics_detail():

    def describe_GET():

        def it_returns_all_properites(client, metric):
            status, content = load(client.get("/api/metrics/id1/2016/11/5"))

            expect(status) == 200
            expect(content) == {
                'PropertyID': "id1",
                'Date': "Sat, 05 Nov 2016 00:00:00 GMT",
                'extra': 42,
            }

        def it_handles_missing_objects(client, metric):
            status, content = load(client.get("/api/metrics/0/1/2/3"))

            expect(status) == 200
            expect(content) == {
                'PropertyID': "0",
                'Date': "Sat, 03 Feb 1 00:00:00 GMT",
            }
