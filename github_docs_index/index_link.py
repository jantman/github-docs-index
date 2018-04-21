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

logger = logging.getLogger(__name__)


class IndexLink(object):
    """
    Base class to represent documents that will be linked in the index page.
    """

    @property
    def sort_datetime(self):
        """
        Return a datetime.datetime instance to be used when sorting documents
        by creation/update time.

        :return: creation/modification time of the document for chronological
          sorting
        :rtype: datetime.datetime
        """
        raise NotImplementedError()

    @property
    def sort_name(self):
        """
        Return a lower-case string to be used as the document title/name when
        sorting documents alphabetically.

        :return: document name/title used for sorting documents alphabetically.
          Should be lower-case.
        :rtype: str
        """
        raise NotImplementedError()

    @property
    def rst_line(self):
        """
        Return the rsStructuredText link/line for this link; this will be used
        as an item in the document list. This should be a hyperlink to the
        document URL with the appropriate title, optionally followed by a
        hyphen and the (~1 sentence) description if available. i.e.:

            `title <http://example.com>`_

        or:

            `title <http://example.com>`_ - Description goes here.

        :return: rst link to document, with optional description
        :rtype: str
        """
        raise NotImplementedError()
