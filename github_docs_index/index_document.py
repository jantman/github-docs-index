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

from textwrap import dedent
import logging

logger = logging.getLogger(__name__)


class IndexDocument(object):
    """Class to represent the actual index document"""

    doc_template = dedent("""
    .. _top:
    
    {title}
    
    < `Chronological Index <#chrono>`_ | `Alphabetical Index <#alpha>`_ >
    
    .. _quicklinks:
    
    Quick Links
    -----------
    
    {quicklinks}
    
    < `top. <#top>`_ | `Quick Links <#quicklinks>`_ | `Alphabetical Index <#alpha>`_ >
    
    .. _chrono:
    
    Chronological Index (most recently updated first)
    -------------------------------------------------
    
    {chrono}
    
    < `top. <#top>`_ | `Quick Links <#quicklinks>`_ | `Chronological Index <#chrono>`_ >
    
    .. _alpha:
    
    Alphabetical Index
    ------------------
    
    {alpha}
    
    < `top. <#top>`_ | `Quick Links <#quicklinks>`_ | `Chronological Index <#chrono>`_ | `Alphabetical Index <#alpha>`_ >
    {footer}
    """)

    def __init__(self, config):
        self._conf = config
        self._repo_links = []
        self._doc = ''

    def add_indexlinks(self, links):
        self._repo_links.extend(links)
        logger.debug('Added %d link instances', len(links))

    def generate_rst(self):
        title = self._conf.title + "\n" + '=' * len(self._conf.title)
        if self._conf.subtitle != '':
            title += '\n\n' + self._conf.subtitle
        footer = ''
        if self._conf.footer != '':
            footer = '\n' + self._conf.footer
        return self.doc_template.format(
            title=title, footer=footer,
            quicklinks='\n'.join([
                '* %s' % ql.rst_line for ql in self._conf.quick_links
            ]),
            chrono='\n'.join([
                '* %s' % r.rst_line for r in sorted(
                    self._repo_links, key=lambda x: x.sort_datetime,
                    reverse=True
                )
            ]),
            alpha='\n'.join([
                '* %s' % r.rst_line for r in sorted(
                    self._repo_links, key=lambda x: x.sort_name
                )
            ])
        )
