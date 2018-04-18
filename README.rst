github-docs-index
=================

.. image:: https://img.shields.io/pypi/v/github-docs-index.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/github-docs-index
   :alt: pypi version

.. image:: https://img.shields.io/github/forks/jantman/github-docs-index.svg
   :alt: GitHub Forks
   :target: https://github.com/jantman/github-docs-index/network

.. image:: https://img.shields.io/github/issues/jantman/github-docs-index.svg
   :alt: GitHub Open Issues
   :target: https://github.com/jantman/github-docs-index/issues

.. image:: https://secure.travis-ci.org/jantman/github-docs-index.png?branch=master
   :target: http://travis-ci.org/jantman/github-docs-index
   :alt: travis-ci for master branch

.. image:: https://codecov.io/github/jantman/github-docs-index/coverage.svg?branch=master
   :target: https://codecov.io/github/jantman/github-docs-index?branch=master
   :alt: coverage report for master branch

.. image:: https://readthedocs.org/projects/github-docs-index/badge/?version=latest
   :target: https://readthedocs.org/projects/github-docs-index/?badge=latest
   :alt: sphinx documentation for latest release

.. image:: http://www.repostatus.org/badges/latest/wip.svg
   :alt: Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.
   :target: http://www.repostatus.org/#wip

Generate a single-page index of documentation hosted in one or more GitHub organizations on github.com and/or one or more GitHub Enterprise instances.

This package is intended for organizations that host their documentation alongside code on GitHub (including GitHub Enterprise) and need a convenient single-page index to help people find things. It's a small, opinionated, and purpose-specific tool, originally written so that my team could have a master index of our documentation (spread across github.com, two GitHub Enterprises, Confluence, and another intranet solution) without having to remember to add every new repository.

Status
------

Pre-alpha. Just planning.

Planned Features
----------------

* Docutils for generation; flexible output to a variety of formats.
* Supports a manually-curated "quick links" section at the top of the page, which can include arbitrary non-GitHub URLs
* Iterates repositories in any number of Organizations (or Users) on github.com and/or any number of GitHub Enterprise instances. Allows blacklisting or whitelisting repositories per-org/user.
* Output sorted alphabetically and/or by last commit date.
* Configurable to show only repositories with GitHub Pages, a Repository URL, repositories with a README file longer than a specified length, repositories with a description, or all repositories.


Requirements
------------

* Python 2.7 or 3.4+ (currently tested with 2.7, 3.4, 3.5, 3.6)
* Python `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv.

.. code-block:: bash

    pip install github-docs-index

Configuration
-------------

Something here.

Usage
-----

Something else here.

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub Issue Tracker <https://github.com/jantman/github-docs-index/issues>`_. Pull requests are
welcome. Issues that don't have an accompanying pull request will be worked on
as my time and priority allows.

Development
===========

To install for development:

1. Fork the `github-docs-index <https://github.com/jantman/github-docs-index>`_ repository on GitHub
2. Create a new branch off of master in your fork.

.. code-block:: bash

    $ virtualenv github-docs-index
    $ cd github-docs-index && source bin/activate
    $ pip install -e git+git@github.com:YOURNAME/github-docs-index.git@BRANCHNAME#egg=github-docs-index
    $ cd src/github-docs-index

The git clone you're now in will probably be checked out to a specific commit,
so you may want to ``git checkout BRANCHNAME``.

Guidelines
----------

* pep8 compliant with some exceptions (see pytest.ini)
* 100% test coverage with pytest (with valid tests)

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <http://tox.testrun.org/>`_.

* testing is as simple as:

  * ``pip install tox``
  * ``tox``

* If you want to pass additional arguments to pytest, add them to the tox command line after "--". i.e., for verbose pytext output on py27 tests: ``tox -e py27 -- -v``

Release Checklist
-----------------

1. Open an issue for the release; cut a branch off master for that issue.
2. Confirm that there are CHANGES.rst entries for all major changes.
3. Ensure that Travis tests passing in all environments.
4. Ensure that test coverage is no less than the last release (ideally, 100%).
5. Increment the version number in github-docs-index/version.py and add version and release date to CHANGES.rst, then push to GitHub.
6. Confirm that README.rst renders correctly on GitHub.
7. Upload package to testpypi:

   * Make sure your ~/.pypirc file is correct (a repo called ``test`` for https://testpypi.python.org/pypi)
   * ``rm -Rf dist``
   * ``python setup.py register -r https://testpypi.python.org/pypi``
   * ``python setup.py sdist bdist_wheel``
   * ``twine upload -r test dist/*``
   * Check that the README renders at https://testpypi.python.org/pypi/github-docs-index

8. Create a pull request for the release to be merged into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -s -a X.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin X.Y.Z``

11. Upload package to live pypi:

    * ``twine upload dist/*``

10. make sure any GH issues fixed in the release were closed.
