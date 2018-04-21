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
from copy import deepcopy
import yaml

from github_docs_index.github_instance import GithubInstance
from github_docs_index.quick_link import QuickLink

logger = logging.getLogger(__name__)


class Config(object):

    def __init__(self, file_path):
        self._yaml = self._load_yaml_config(file_path)
        self._githubs = []
        self._ignore_forks = False
        self._quick_links = []
        self._repo_criteria = []
        self._validate_config()
        logger.info('Configuration loaded from: %s', file_path)

    def _load_yaml_config(self, file_path):
        logger.debug('Reading config file from: %s', file_path)
        with open(file_path, 'r') as fh:
            return yaml.load(fh)

    def _validate_config(self):
        if not isinstance(self._yaml, type({})):
            raise RuntimeError(
                'ERROR: YAML configuration must be a mapping type.'
            )
        self._load_githubs()
        self._load_quick_links()
        self._load_repo_criteria()
        if 'ignore_forks' in self._yaml:
            if not isinstance(self._yaml['ignore_forks'], type(True)):
                raise RuntimeError(
                    'Configuration key "ignore_forks" must be boolean.'
                )
            self._ignore_forks = self._yaml['ignore_forks']
        if 'title' in self._yaml:
            self._title = self._yaml['title']
        else:
            self._title = 'Documentation Index'
        self._footer = ''
        if 'footer' in self._yaml:
            self._footer = self._yaml['footer']
        if 'GITHUB_DOCS_FOOTER' in os.environ:
            self._footer = os.environ['GITHUB_DOCS_FOOTER']
        self._subtitle = ''
        if 'subtitle' in self._yaml:
            self._subtitle = self._yaml['subtitle']
        if 'GITHUB_DOCS_SUBTITLE' in os.environ:
            self._subtitle = os.environ['GITHUB_DOCS_SUBTITLE']

    def _load_githubs(self):
        keys = [
            'url', 'token_env_var', 'orgs', 'users', 'blacklist_repos',
            'whitelist_repos', 'blacklist_orgs'
        ]
        blank = {
            'url': 'https://api.github.com',
            'orgs': [],
            'users': [],
            'blacklist_repos': [],
            'whitelist_repos': [],
            'blacklist_orgs': []
        }
        for g in self._yaml['githubs']:
            if not set(g.keys()).issubset(set(keys)):
                raise RuntimeError(
                    'ERROR: invalid keys in github configuration: %s' % g
                )
            d = deepcopy(blank)
            d.update(g)
            self._githubs.append(GithubInstance(self, **d))
        logger.debug('Loaded %d GitHubs', len(self._githubs))

    def _load_quick_links(self):
        for link in self._yaml['quick_links']:
            self._quick_links.append(QuickLink(**link))
        logger.debug('Loaded %d Quick Links', len(self._quick_links))

    def _load_repo_criteria(self):
        self._repo_criteria = self._yaml['repo_criteria']

    @property
    def as_dict(self):
        return {
            'githubs': [g.as_dict for g in self._githubs],
            'ignore_forks': self._ignore_forks,
            'quick_links': [l.as_dict for l in self._quick_links],
            'repo_criteria': self._repo_criteria
        }

    @property
    def githubs(self):
        """
        Return a list of configured GitHub Instances to poll.

        :returns: list of GitHub instances to poll.
        :rtype: ``list`` of :py:class:`~.GithubInstance`
        """
        return self._githubs

    @property
    def ignore_forks(self):
        """
        Return whether or not the index generator should ignore forks.

        :returns: whether or not forks should be ignored
        :rtype: bool
        """
        return self._ignore_forks

    @property
    def quick_links(self):
        """
        Return a list of dicts representing Quick Links to add to the top of
        the index document.

        :returns: list of quick link dicts
        :rtype: ``list`` of ``dict``
        """
        return self._quick_links

    @property
    def repo_criteria(self):
        """
        Return the list of repository criteria for inclusion in index.

        :returns: repository criteria
        :rtype: ``list``
        """
        return self._repo_criteria

    @property
    def title(self):
        return self._title

    @property
    def footer(self):
        return self._footer

    @property
    def subtitle(self):
        return self._subtitle
