# -*- coding: utf-8 -*-

import pytest


def pytest_addoption(parser):
    group = parser.getgroup('validate')
    group.addoption(
        '--foo',
        action='store',
        dest='dest_foo',
        default='2020',
        help='Set the value for the fixture "bar".'
    )


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
