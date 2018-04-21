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

import sys
import argparse
import logging

from github_docs_index.version import VERSION, PROJECT_URL
from github_docs_index.config import Config
from github_docs_index.index_generator import GithubDocsIndexGenerator

logger = logging.getLogger(__name__)

# suppress requests logging
for lname in ['github3', 'urllib3']:
    l = logging.getLogger(lname)
    l.setLevel(logging.WARNING)
    l.propagate = True


def parse_args(argv):
    p = argparse.ArgumentParser(
        description='GitHub Documentation index generator'
    )
    p.add_argument('-v', '--verbose', dest='verbose', action='count', default=0,
                   help='verbose output. specify twice for debug-level output.')
    p.add_argument('-V', '--version', action='version',
                   version='github_docs_index v%s <%s>' % (
                       VERSION, PROJECT_URL
                   ))
    p.add_argument('CONFIG_FILE', action='store',
                   help='Path to config.yaml file')
    args = p.parse_args(argv)
    return args


def set_log_info(logger):
    """
    set logger level to INFO via :py:func:`~.set_log_level_format`.
    """
    set_log_level_format(logger, logging.INFO,
                         '%(asctime)s %(levelname)s:%(name)s:%(message)s')


def set_log_debug(logger):
    """
    set logger level to DEBUG, and debug-level output format,
    via :py:func:`~.set_log_level_format`.
    """
    set_log_level_format(
        logger,
        logging.DEBUG,
        "%(asctime)s [%(levelname)s %(filename)s:%(lineno)s - "
        "%(name)s.%(funcName)s() ] %(message)s"
    )


def set_log_level_format(logger, level, format):
    """
    Set logger level and format.

    :param logger: the logger object to set on
    :type logger: logging.Logger
    :param level: logging level; see the :py:mod:`logging` constants.
    :type level: int
    :param format: logging formatter format string
    :type format: str
    """
    formatter = logging.Formatter(fmt=format)
    logger.handlers[0].setFormatter(formatter)
    logger.setLevel(level)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    global logger
    format = "[%(asctime)s %(levelname)s] %(message)s"
    logging.basicConfig(level=logging.WARNING, format=format)
    logger = logging.getLogger()

    args = parse_args(argv)

    # set logging level
    if args.verbose > 1:
        set_log_debug(logger)
    elif args.verbose == 1:
        set_log_info(logger)

    conf = Config(args.CONFIG_FILE)
    g = GithubDocsIndexGenerator(conf)
    print(g.generate_index())


if __name__ == "__main__":
    main(argv=sys.argv[1:])
