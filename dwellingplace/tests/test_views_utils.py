# pylint: disable=unused-argument,unused-variable,expression-not-assigned

from expecter import expect
from freezegun import freeze_time

from dwellingplace.views._utils import get_filename


def describe_get_filename():

    @freeze_time("2016-11-06 10:19:30")
    def it_adds_a_timestamp():
        expect(get_filename("myfile", "myext")) == \
            "/tmp/myfile-2016-11-06-10-19-30.myext"
