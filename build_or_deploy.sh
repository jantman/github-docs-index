#!/bin/bash -x
# github-docs-index build and release script
################################################################################
# The latest version of this package is available at:
#<http://github.com/jantman/github-docs-index>
#
################################################################################
#Copyright 2017 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
#
#    This file is part of github-docs-index.
#
#    github-docs-index is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    github-docs-index is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with github-docs-index.  If not, see <http://www.gnu.org/licenses/>.
#
#The Copyright and Authors attributions contained herein may not be removed or
#otherwise altered, except to add the Author attribution of a contributor to
#this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
#While not legally required, I sincerely request that anyone who finds
#bugs please submit them at <https://github.com/jantman/github-docs-index> or
#to me via email, and that you send any contributions or improvements
#either as a pull request on GitHub, or to me via email.
################################################################################
#
#AUTHORS:
#Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################

set -x
set -e

if [ -z "$1" ]; then
    >&2 echo "USAGE: build_or_deploy.sh [build|push]"
    exit 1
fi

function gettag {
    # if it's a build of a tag, return that right away
    [ ! -z "$TRAVIS_TAG" ] && { echo $TRAVIS_TAG; return 0; }
    # otherwise, prefix with PR number if available
    prefix=''
    [ ! -z "$TRAVIS_PULL_REQUEST" ] && [[ "$TRAVIS_PULL_REQUEST" != "false" ]] && prefix="PR${TRAVIS_PULL_REQUEST}_"
    ref="test_${prefix}$(git rev-parse --short HEAD)_$(date +%s)"
    echo "${ref}"
}

function getversion {
    python -c 'from github_docs_index.version import VERSION; print(VERSION)'
}

function pythonbuild {
    rm -Rf dist
    python setup.py sdist bdist_wheel
    ls -l dist
}

function pythonpush {
    pip install twine
    twine upload dist/*
}

if [[ "$1" == "build" ]]; then
    pythonbuild
elif [[ "$1" == "push" ]]; then
    pythonpush
else
    >&2 echo "USAGE: build_or_deploy.sh [build|push]"
    exit 1
fi
