# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from expecter import expect

from dwellingplace.models import Metric


def describe_metrics():

    def describe_init():

        def it_does_a_thing():
            m = Metric()
            expect(m) == m
