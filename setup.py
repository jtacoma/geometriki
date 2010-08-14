# This file is part of geometriki.
#
# geometriki is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# geometriki is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with geometriki, in a file named COPYING. If not,
# see <http://www.gnu.org/licenses/>.
"""A collaborative JavaScript development environment.

**geometriki** is a **wiki** in which each page can be processed either
for people to read (HTML, PDF) or for machines to process (**JSON** or
**JavaScript**).  As a result, it is effectively a collaborative
development environment for JavaScript applications, especially those
that can be useful without frequent updates to server-side data.
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='geometriki',
    version='0.1.9',
    description='A collaborative JavaScript development environment.',
    author='Joshua Tacoma',
    author_email='joshua@yellowseed.org',
    url='http://gitorious.org/geometriki',
    install_requires=[
        "Pylons>=1.0",
        "python-openid",
        "docutils",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'geometriki': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'geometriki': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = geometriki.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Pylons",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    long_description='\n'.join(__doc__.split('\n')[2:]),
)
