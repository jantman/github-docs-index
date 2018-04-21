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

from datetime import datetime
import logging

from github_docs_index.index_link import IndexLink

logger = logging.getLogger(__name__)


class RepoLink(IndexLink):
    """
    Represents one repository that should be linked to in the docs index.
    """

    def __init__(
        self, owner_name, repo_name, url, description=None,
        last_commit_datetime=None
    ):
        self._owner_name = owner_name
        self._repo_name = repo_name
        self._url = url
        self._description = description
        self._last_commit_datetime = last_commit_datetime

    @property
    def as_dict(self):
        if hasattr(self._last_commit_datetime, 'timestamp'):
            ts = self._last_commit_datetime.timestamp()
        else:
            # python < 3.3
            naive = self._last_commit_datetime.replace(tzinfo=None) - \
                self._last_commit_datetime.utcoffset()
            ts = (naive - datetime(1970, 1, 1)).total_seconds()
        return {
            'owner_name': self._owner_name,
            'repo_name': self._repo_name,
            'url': self._url,
            'description': self._description,
            'last_commit_timestamp': ts
        }

    def set_last_commit_datetime(self, dt):
        if not isinstance(dt, type(datetime(1970, 1, 2))):
            raise RuntimeError(
                'ERROR: argument to set_last_commit_datetime() must be a '
                'datetime instance, not a %s (value: "%s")' % (
                    type(dt), dt
                )
            )
        self._last_commit_datetime = dt

    def set_description(self, desc):
        self._description = desc

    @property
    def lower_case_full_name(self):
        return '%s/%s' % (self._owner_name.lower(), self._repo_name.lower())

    @property
    def full_name(self):
        return '%s/%s' % (self._owner_name, self._repo_name)

    @property
    def description(self):
        if self._description is not None and self._description.strip() == '':
            return None
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def sort_datetime(self):
        return self._last_commit_datetime

    @property
    def sort_name(self):
        return self._repo_name.lower()

    @property
    def rst_line(self):
        if self.description is None:
            return '`%s <%s>`_' % (self._repo_name, self.url)
        return '`%s <%s>`_ - %s' % (self._repo_name, self.url, self.description)
