"""
The latest version of this package is available at:
<http://github.com/jantman/github-docs-index>

##################################################################################
Copyright 2018 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of github-docs-index, also known as github-docs-index.

    github-docs-index is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    github-docs-index is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with github-docs-index.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/github-docs-index> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

import logging

try:
    from unittest.mock import patch, call, Mock
except ImportError:
    from mock import patch, call, Mock

from github_docs_index.runner import (
    set_log_debug, set_log_info, set_log_level_format, parse_args
)

pbm = 'github_docs_index.runner'


class MockArgs(object):

    def __init__(self, **kwargs):
        self.verbose = 0
        self.ACTION = None
        self.SCHEDULES = []
        self.only_email_if_problems = False
        for k, v in kwargs.items():
            setattr(self, k, v)


class TestParseArgs(object):

    def test_parse_args_default(self):
        res = parse_args(
            ['foo/bar.yaml']
        )
        assert res.verbose == 0
        assert res.CONFIG_FILE == 'foo/bar.yaml'

    def test_parse_args_info(self):
        res = parse_args(
            ['-v', 'foo/bar.yaml']
        )
        assert res.verbose == 1
        assert res.CONFIG_FILE == 'foo/bar.yaml'

    def test_parse_args_debug(self):
        res = parse_args(
            ['-vv', 'foo/bar.yaml']
        )
        assert res.verbose == 2
        assert res.CONFIG_FILE == 'foo/bar.yaml'


class TestLogSetup(object):

    def test_set_log_info(self):
        m_log = Mock()
        with patch('%s.set_log_level_format' % pbm) as mock_set:
            set_log_info(m_log)
        assert mock_set.mock_calls == [
            call(
                m_log, logging.INFO,
                '%(asctime)s %(levelname)s:%(name)s:%(message)s'
            )
        ]

    def test_set_log_debug(self):
        m_log = Mock()
        with patch('%s.set_log_level_format' % pbm) as mock_set:
            set_log_debug(m_log)
        assert mock_set.mock_calls == [
            call(m_log, logging.DEBUG,
                 "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
                 "%(name)s.%(funcName)s() ] %(message)s")
        ]

    def test_set_log_level_format(self):
        m_log = Mock()
        mock_handler = Mock(spec_set=logging.Handler)
        with patch('%s.logging.Formatter' % pbm) as mock_formatter:
            type(m_log).handlers = [mock_handler]
            set_log_level_format(m_log, 5, 'foo')
        assert mock_formatter.mock_calls == [
            call(fmt='foo')
        ]
        assert mock_handler.mock_calls == [
            call.setFormatter(mock_formatter.return_value)
        ]
        assert m_log.mock_calls == [
            call.setLevel(5)
        ]
