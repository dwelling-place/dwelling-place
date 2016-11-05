# pylint: disable=unused-variable,unused-argument,expression-not-assigned,singleton-comparison

from expecter import expect

from dwellingplace.models import Foobar


def describe_foobar():

    def describe_init():

        def it_does_a_thing():
            foobar = Foobar()
            expect(foobar) == foobar
