==========
geometriki
==========

Installation and Setup
======================

Install ``geometriki`` using easy_install::

    easy_install geometriki

Make a config file as follows::

    paster make-config geometriki config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.

Deployment
==========

Run the ``geometriki`` in its own web server::

    paster serve config.ini

If you want to do something more specific, see `Pylons Cookbook: Deployment`_ or `Pylons Book v1.1: Chapter 21: Deployment`_.

.. _`Pylons Book v1.1: Chapter 21: Deployment`: http://pylonsbook.com/en/1.1/deployment.html
.. _`Pylons Cookbook: Deployment`: http://wiki.pylonshq.com/display/pylonscookbook/Deployment
