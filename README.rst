github-docs-index
=================

.. image:: https://img.shields.io/pypi/v/github-docs-index.svg?maxAge=2592000
   :target: https://pypi.org/project/github-docs-index
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

**Full documentation is available on ReadTheDocs:** http://github-docs-index.readthedocs.io/en/latest/

Features
--------

* Outputs docutils-ready reStructuredText for processing or conversion to a variety of formats.
* Supports a manually-curated "quick links" section at the top of the page, which can include arbitrary non-GitHub URLs
* Iterates repositories in any number of Organizations (or Users) on github.com and/or any number of GitHub Enterprise instances. Allows blacklisting or whitelisting repositories per-org/user and blacklisting organizations.
* Output sorted alphabetically and by last commit/update date.
* Configurable to show only repositories with GitHub Pages, a Repository URL, repositories with a README file longer than a specified length, repositories with a description, or all repositories.
* Option to ignore forks.
* Python API which allows injecting additional links to the chronological and alphabetical lists.
* GitHub tokens taken from environment variables.
* Configurable title, subtitle/header and footer; subtitle and footer can be overridden by environment variables.

Requirements
------------

* Python 2.7 or 3.4+ (currently tested with 2.7, 3.4, 3.5, 3.6)
* `VirtualEnv <http://www.virtualenv.org/>`_ and ``pip`` (recommended installation method; your OS/distribution should have packages for these)

Installation
------------

It's recommended that you install into a virtual environment (virtualenv /
venv). See the `virtualenv usage documentation <http://www.virtualenv.org/en/latest/>`_
for information on how to create a venv.

.. code-block:: bash

    pip install github-docs-index

Configuration
-------------

Configuration is provided by a YAML file; see `example_config.yaml <example_config.yaml>`_ for a detailed example. The YAML file must have a mapping/hash/dict at the top level. Keys are as follows:

* **title**, string, the title of the index rst document
* **footer**, *optional*, string, a footer line to include at the end of the index rst document. This configuration option is overridden by the ``GITHUB_DOCS_FOOTER`` environment variable if set.
* **subtitle**, *optional*, string, a subtitle/header line to include below the title of the index rst document. This configuration option is overridden by the ``GITHUB_DOCS_SUBTITLE`` environment variable if set.
* **githubs**, array/list of mappings/dicts specifying the github instances to query. Each item in the array has the following structure:

  * **token_env_var**, string, name of the environment variable that contains the Personal Access Token for this github instance
  * **url**, *optional*, string, URL to this GitHub instance for GitHub Enterprise instances. If not specified, defaults to ``https://api.github.com``
  * **orgs**, *optional*, array of string organization names to scan repositories in. If neither this option nor "orgs" is specified, default to scanning all repos of orgs that the authenticated user belongs to.
  * **users**, *optional*, array of string user names to scan repositories in. If neither this option nor "orgs" is specified, default to scanning all repos of orgs that the authenticated user belongs to.
  * **whitelist_repos**, *optional*, array of string repository slugs (full names) in "owner_name/repo_name" format. If specified, only these repos will be included regardless of other configuration for this GitHub instance.
  * **blacklist_repos**, *optional*, array of string repository slugs (full names) in "owner_name/repo_name" format to never include in the output documentation index.
  * **blacklist_orgs**, *optional*, array of string organization names to ignore when scanning repos.

* **ignore_forks**, *optional*, boolean, default False. If True, do not include any repos that are forks in the listing.
* **quick_links**, *optional*, array/list of mappings/dicts specifying manually-curated links to add to the "Quick Links" section at the top of the document. Each item in the array has the following structure:

  * **title** string, the title/text of the link
  * **url** string, the URL to link to
  * **description**, *optional*, string description to output after the link to the repo

* **repo_criteria**, array/list of strings or mappings determining which repos to include in the listing and what URL to set for them. For each repo, these are evaluated in order and the first match wins; if none match, the repo is not added to the list. Possible options are:

  * ``homepage``, string: if present, use the Repository Homepage URL (at the top of the repo page, next to the description) as the link. Only matches repos with a Homepage set.
  * ``github_pages``, string: if present, use the repo's GitHub Pages URL as the link. Only matches repos with GitHub Pages enabled.
  * ``readme: N``, mapping/dict where "readme" is a string and N is an integer: match repos with a readme file of size N or greater, and link to the repo's main HTML URL (github web UI URL)
  * ``description``, string: match any repo with a description set, and link to the repo's main HTML URL (github web UI URL)
  * ``all`` match any/all repos, and link to the repo's main HTML URL (github web UI URL)

CLI Usage
---------

Usage via the command line is straightforward for common use cases. The reStructuredText output is printed to STDOUT, and can be redirected to a file. For example, assuming you've already installed the package as shown above, and using ``example_config.yaml`` as an example:

.. code-block:: bash

    # these next three environment variable names are specified in example_config.yaml
    export GITHUB_TOKEN=yourToken
    export GHE_TOKEN=anotherToken
    export OTHER_GHE_TOKEN=yetAnotherToken
    github-docs-index config.yaml > index.rst

This rst file can be converted to the format of your choice with any tool that understands reStructuredText input. For example, it can be converted to HTML using ``rst2html.py`` from the `docutils <http://docutils.sourceforge.net>`_ package (``pip install docutils``):

.. code-block:: bash

    rst2html.py --report=4 index.rst > index.html

Setting Subtitle and Footer
---------------------------

The optional subtitle (line below the title) and footer (line at the bottom of the document) can also be specified as environment variables. For example:

.. code-block:: bash

    export GITHUB_DOCS_SUBTITLE="This document was automatically generated at $(date)"
    export GITHUB_DOCS_FOOTER="This document was generated by Jenkins: ${BUILD_URL}"
    github-docs-index config.yaml > index.rst

Example Output
--------------

You can see an example of the actual HTML output for my own github user in the source tree at `example_output.rst <example_output.rst>`_.

Python Usage
------------

github-docs-index can also be imported and used in other Python code. This can be especially useful for doing something with the raw rst output; here is an example that replicates the functionality of the above CLI examples in a single Python script:

.. code-block:: python

   #!/usr/bin/env python

   # for generating the rst
   from github_docs_index.config import Config
   from github_docs_index.index_generator import GithubDocsIndexGenerator

   # for docutils rst -> HTML
   from docutils import core
   from docutils.writers.html4css1 import Writer, HTMLTranslator


   # this replicates "github-docs-index config.yaml" at the command line
   g = GithubDocsIndexGenerator(Config('config.yaml'))
   rst_string = g.generate_index()

   # the code below here replicates "rst2html.py --report=4 index.rst > index.html"


   class HTMLFragmentTranslator(HTMLTranslator):

       def __init__(self, document):
           HTMLTranslator.__init__(self, document)
           self.head_prefix = ['', '', '', '', '']
           self.body_prefix = []
           self.body_suffix = []
           self.stylesheet = []

       def astext(self):
           return ''.join(self.body)


   html_fragment_writer = Writer()
   html_fragment_writer.translator_class = HTMLFragmentTranslator

   with open('index.html', 'wb') as fh:
       fh.write(core.publish_string(rst_string, writer=html_fragment_writer))
   print('Output written to: index.html')

Adding Documentation From Other Sources
+++++++++++++++++++++++++++++++++++++++

It's also possible via the Python API to include aribtrary documents from sources other than GitHub in the index; they will be sorted into the chronological and alphabetical lists along with the GitHub repositories. This can be helpful if you have other sources of documentation such as an Intranet or Wiki that you can programmatically query. The only requirement is that each document has a URL, title, date (generally a created/modified/updated date) and optional short description. The `GithubDocsIndexGenerator.generate_index <http://github-docs-index.readthedocs.io/en/latest/github_docs_index.index_generator.html#github_docs_index.index_generator.GithubDocsIndexGenerator.generate_index>`_ method takes an optional ``additional_links`` argument which is a list of instances of a subclass of `github_docs_index.index_link.IndexLink <http://github-docs-index.readthedocs.io/en/latest/github_docs_index.index_link.html#github_docs_index.index_link.IndexLink>`_. So long as the instances implement the three properties of ``IndexLink``, they will be included in the documentation index. Here is a short, contrived example based on the code above which includes two other documents with hard-coded dates, titles and URLs; the ``generate_additional_links()`` function could be switched out for one which queries your alternate documentation stores and returns similar output.

.. code-block:: python

   #!/usr/bin/env python3

   from datetime import datetime, timezone
   from github_docs_index.config import Config
   from github_docs_index.index_generator import GithubDocsIndexGenerator
   from github_docs_index.index_link import IndexLink


   class StaticLink(IndexLink):
       """This class implements the three property methods in IndexLink"""

       def __init__(self, title, url, sort_datetime, description=''):
           self._title = title
           self._url = url
           self._sort_datetime = sort_datetime
           self._description = description

       @property
       def sort_datetime(self):
           return self._sort_datetime

       @property
       def sort_name(self):
           return self._title.lower()

       @property
       def rst_line(self):
           r = '`%s <%s>`_' % (self._title, self._url)
           if self._description is not None and self._description.strip() != '':
               r += ' - ' + self._description
           return r


   def generate_additional_links():
       return [
           StaticLink(
               'Some Document', 'http://example.com/someDocument',
               datetime(2017, 6, 3, 12, 34, 41, tzinfo=timezone.utc),
               description='this is a document'
           ),
           StaticLink(
               'Other Document', 'http://example.com/otherDocument',
               datetime(2018, 8, 12, 19, 24, 53, tzinfo=timezone.utc),
               description='this is another document'
           )
       ]


   # this replicates "github-docs-index config.yaml" at the command line
   g = GithubDocsIndexGenerator(Config('config.yaml'))
   rst_string = g.generate_index(additional_links=generate_additional_links())

   with open('index.rst', 'w') as fh:
       fh.write(rst_string)

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

Testing is done via `pytest <http://pytest.org/latest/>`_, driven by `tox <https://tox.readthedocs.io/en/latest/>`_.

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

   * Make sure your ~/.pypirc file is correct (a repo called ``test`` for https://test.pypi.org/)
   * ``rm -Rf dist``
   * ``python setup.py sdist bdist_wheel``
   * ``twine upload -r test dist/*``
   * Check that the README renders at https://test.pypi.org/project/github-docs-index

8. Create a pull request for the release to be merged into master. Upon successful Travis build, merge it.
9. Tag the release in Git, push tag to GitHub:

   * tag the release. for now the message is quite simple: ``git tag -s -a X.Y.Z -m 'X.Y.Z released YYYY-MM-DD'``
   * push the tag to GitHub: ``git push origin X.Y.Z``

11. TravisCI will cut the release and upload to PyPI.
