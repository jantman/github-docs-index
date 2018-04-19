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

logger = logging.getLogger(__name__)


class GithubInstance(object):

    def __init__(self, token_env_var, url='https://api.github.com', users=[],
                 orgs=[], blacklist_repos=[], whitelist_repos=[]):
        self._token_env_var = token_env_var
        self._token = os.environ[self._token_env_var]
        self._url = url
        self._users = users
        self._orgs = orgs
        self._blacklist_repos = blacklist_repos
        self._whitelist_repos = whitelist_repos

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
        iterate over each org
        for each org, iterate over each repo not in blacklist, or if
           whitelist is specified, only those repos.
        create RepoLink instances for each repo that matches our criteria.
        return the list of RepoLink instances
        """
        # if self._users is [] and self._orgs is [], and no whitelist,
        # default to all orgs we're a member of
        pass
