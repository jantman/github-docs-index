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
                 users=[], orgs=[], blacklist_repos=[], whitelist_repos=[],
                 blacklist_orgs=[]):
        self._conf = config
        self._token_env_var = token_env_var
        self._token = os.environ[self._token_env_var]
        self._url = url
        self._users = users
        self._orgs = orgs
        self._blacklist_repos = blacklist_repos
        self._whitelist_repos = whitelist_repos
        self._blacklist_orgs = blacklist_orgs
        if self._url == 'https://api.github.com':
            self._gh = login(token=self._token)
        else:
            self._gh = enterprise_login(url=self._url, token=self._token)
        self._current_user = self._gh.me()
        self._login = self._current_user.login
        logger.info(
            'Authenticated to %s as user %s', self._url, self._login
        )

    @property
    def as_dict(self):
        return {
            'token_env_var': self._token_env_var,
            'url': self._url,
            'orgs': self._orgs,
            'users': self._users,
            'whitelist_repos': self._whitelist_repos,
            'blacklist_repos': self._blacklist_repos,
            'blacklist_orgs': self._blacklist_orgs
        }

    def _get_orgs_for_current_user(self):
        """
        Return a list of Organizations that the current user is a member of.

        :return: Organization names/logins
        :rtype: ``list``
        """
        logger.debug('Listing organization membership for current user')
        return [o.login for o in self._gh.organizations()]

    def get_docs_repos(self):
        """
        Iterate over all specified users/orgs and identify all suitable repos.
        Return a list of :py:class:`~.RepoLink` instances for all repos that
        match the configured criteria.

        :returns: all repos that should be included in the index
        :rtype: ``list`` of :py:class:`~.RepoLink` objects.
        """
        logger.debug(
            'Iterating selected users and orgs as %s on %s',
            self._login, self._url
        )
        if len(self._users) == 0 and len(self._orgs) == 0:
            logger.debug(
                'No users or orgs specified for %s; using all orgs that %s'
                ' is a member of', self._url, self._login
            )
            self._orgs = self._get_orgs_for_current_user()
            logger.debug('Orgs to search: %s', self._orgs)
        all_repos = []
        # add all user repos to list
        for username in self._users:
            logger.debug('Iterating repos for user: %s', username)
            for repo in self._gh.repositories_by(username, type='owner'):
                all_repos.append(
                    self._gh.repository(repo.owner.login, repo.name)
                )
        # add all org repos to list
        for orgname in self._orgs:
            if orgname in self._blacklist_orgs:
                logger.debug('Ignoring blacklisted org: %s', orgname)
                continue
            logger.debug('Iterating repos for organization: %s', orgname)
            org = self._gh.organization(orgname)
            for repo in org.repositories(type='all'):
                all_repos.append(
                    self._gh.repository(repo.owner.login, repo.name)
                )
        # now check each repo, and add to results as appropriate
        results = []
        logger.debug(
            'Checking all %d repos for match against configured criteria',
            len(all_repos)
        )
        for repo in all_repos:
            if repo.full_name in self._blacklist_repos:
                logger.debug(
                    'Skipping blacklisted repo: %s', repo.full_name
                )
                continue
            if (
                self._whitelist_repos != [] and
                repo.full_name not in self._whitelist_repos
            ):
                logger.debug(
                    'Skipping non-whitelisted repo: %s', repo.full_name
                )
                continue
            if self._conf.ignore_forks and repo.fork:
                logger.debug('Skipping fork: %s', repo.full_name)
                continue
            tmp = self._check_repo_criteria(repo)
            if tmp is not None:
                results.append(tmp)
        logger.info(
            'Found %d repos as %s on %s that match configured criteria',
            len(results), self._login, self._url
        )
        return results

    def _check_repo_criteria(self, repo):
        """
        Given a github3 Repository object, iterate through the configured
        repo criteria (:py:attr:`~.Config.repo_criteria`) calling
        :py:meth:`~._check_single_criterion` for each. Return the first
        non-None result, or None.

        :param repo: the repository to check
        :type repo: github3.repos.repo.Repository
        :return: Information for repository link, or None
        :rtype: ``None`` or :py:class:`~.RepoLink`
        """
        logger.debug('Checking if repo meets criteria: %s', repo.full_name)
        for criterion in self._conf.repo_criteria:
            tmp = self._check_single_criterion(repo, criterion)
            if tmp is not None:
                logger.debug(
                    'Repo %s matched criterion: %s', repo.full_name, criterion
                )
                return tmp
        logger.debug('Repo %s did not match any criteria.', repo.full_name)
        return None

    def _repolink_for_pages(self, repo):
        """
        Return a RepoLink pointing to the Github Pages site for the specified
        repo. The `Pages API <https://developer.github.com/v3/repos/pages/>`_
        is currently in Developer Preview (as of 2018-04-21) and requires a
        special Accept header to be sent in order to return the ``html_url``
        field.

        :param repo: repository
        :type repo: github3.repos.repo.Repository
        :return: RepoLink instance pointing to the repo's Github Pages URL
        :rtype: RepoLink
        """
        oldaccept = self._gh.session.headers.get('Accept', None)
        self._gh.session.headers[
            'Accept'
        ] = 'application/vnd.github.mister-fantastic-preview+json'
        try:
            pages = repo.pages()
            self._gh.session.headers['Accept'] = oldaccept
            html_url = pages._json_data['html_url']
        except KeyError:
            raise RuntimeError(
                'GitHub repository/pages API did not return "html_url" field; '
                'it appears this package needs to be updated for changes to '
                'the GitHub API.'
            )
        except Exception:
            self._gh.session.headers['Accept'] = oldaccept
            raise
        return RepoLink(repo.owner.login, repo.name, html_url)

    def _check_single_criterion(self, repo, criterion):
        """
        Given a github3 Repository object and a criterion (entry in the
        ``repo_criteria`` configuration list as returned by
        :py:attr:`~.Config.repo_criteria`), return an appropriate
        :py:class:`~.RepoLink` object if the repo matches the criterion, or None
        otherwise.

        :param repo: the repository to check
        :type repo: github3.repos.repo.Repository
        :param criterion: the criterion to check the repo against
        :type criterion: ``str`` or ``dict``
        :return: a RepoLink for the repo if it matches the criterion, or else
          None
        :rtype: :py:class:`~.RepoLink` or ``None``
        """
        rlink = None
        if criterion == 'homepage':
            if repo.homepage is None or repo.homepage == '':
                return None
            rlink = RepoLink(repo.owner.login, repo.name, repo.homepage)
        elif criterion == 'github_pages':
            if not repo.has_pages:
                return None
            rlink = self._repolink_for_pages(repo)
        elif isinstance(criterion, type({})) and 'readme' in criterion:
            readme_len = criterion.get('readme', None)
            if not isinstance(readme_len, type(12)):
                raise RuntimeError('"readme" criterion must have an int value')
            try:
                readme = repo.readme()
            except Exception:
                return None
            if readme.size < readme_len:
                return None
            rlink = RepoLink(repo.owner.login, repo.name, repo.html_url)
        elif criterion == 'description':
            if repo.description is None or repo.description.strip() == '':
                return None
            rlink = RepoLink(repo.owner.login, repo.name, repo.html_url)
        elif criterion == 'all':
            rlink = RepoLink(repo.owner.login, repo.name, repo.html_url)
        else:
            raise RuntimeError('Invalid criterion: %s', criterion)
        if rlink is None:
            return rlink
        # RepoLink exists; update with common information
        if repo.description not in [None, '']:
            rlink.set_description(repo.description)
        rlink.set_last_commit_datetime(repo.updated_at)
        return rlink
