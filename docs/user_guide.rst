==========
User Guide
==========

Installation and Setup
======================

Install Python_ and setuptools_.

Install ``geometriki`` using easy_install::

    easy_install geometriki

Make a config file as follows::

    paster make-config geometriki config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.  To see what it looks like you can run::

    paster serve config.ini

For more about deploying this application to a web server, see `Chapter 21: Deployment`_ in the `Pylons Book`_.

.. _Python: http://www.python.org/download/releases/2.7/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _`Chapter 21: Deployment`: http://pylonsbook.com/en/1.1/deployment.html
.. _`Pylons Book`: http://pylonsbook.com/en/1.1/index.html