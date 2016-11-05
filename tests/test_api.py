# pylint: disable=unused-variable,unused-argument,expression-not-assigned

from expecter import expect

from .utils import load


def describe_metrics_detail():

    def describe_GET():

        def it_returns_all_properites(client, metric):
            status, content = load(client.get("/api/metrics/id1/2016"))

            expect(status) == 200
            expect(content) == {
                'PropertyID': "id1",
                'Date': "2016",
                'extra': 42,
            }

        def it_handles_missing_objects(client, metric):
            status, content = load(client.get("/api/metrics/not/there"))

            expect(status) == 200
            expect(content) == {
                'PropertyID': "not",
                'Date': "there",
            }
