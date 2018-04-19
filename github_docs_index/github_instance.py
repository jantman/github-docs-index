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

import os
import logging
from github3 import login, enterprise_login

from github_docs_index.repo_link import RepoLink

logger = logging.getLogger(__name__)


class GithubInstance(object):

    def __init__(self, config, token_env_var, url='https://api.github.com',
                 users=[], orgs=[], blacklist_repos=[], whitelist_repos=[]):
        self._conf = config
        self._token_env_var = token_env_var
        self._token = os.environ[self._token_env_var]
        self._url = url
        self._users = users
        self._orgs = orgs
        self._blacklist_repos = blacklist_repos
        self._whitelist_repos = whitelist_repos
        if self._url == 'https://api.github.com':
            self._gh = login(token=self._token)
        else:
            self._gh = enterprise_login(url=self._url, token=self._token)

    @property
    def as_dict(self):
        return {
            'token_env_var': self._token_env_var,
            'url': self._url,
            'orgs': self._orgs,
            'users': self._users,
            'whitelist_repos': self._whitelist_repos,
            'blacklist_repos': self._blacklist_repos
        }

    def get_docs_repos(self):
        """
        Iterate over all specified users/orgs and identify all suitable repos.
        Return a list of :py:class:`~.RepoLink` instances for all repos that
        match the configured criteria.

        :returns: all repos that should be included in the index
        :rtype: ``list`` of :py:class:`~.RepoLink` objects.
        """
        if len(self._users) == 0 and len(self._orgs) == 0:
            logger.debug(
                'No users or orgs specified; using all orgs that current'
                ' user/token is a member of'
            )
            self._orgs = self._get_orgs_for_token()
            logger.debug('Orgs to search: %s', self._orgs)
        # if self._users is [] and self._orgs is [], and no whitelist,
        # default to all orgs we're a member of
        # iterate over each org
        # iterate over each repo in org, respecting whitelist/blacklist
        pass
