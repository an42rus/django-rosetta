Installation
============

Requirements
------------
* As of version 0.7.13, Rosetta supports Django 1.8 through 1.11.


Install Rosetta
---------------

1. ``pip install django-rosetta``
2. Add ``'rosetta'`` to the `INSTALLED_APPS` in your project's ``settings.py``
3. Add an URL entry to your project's ``urls.py``, for example::

    from django.conf import settings

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls')),
        )
Note: you can use whatever you wish as the URL prefix.

4. To get translations by lang_code from Angular framework add an URL entry to your project's ``urls.py``, for example::

    from django.conf import settings

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^api/translations/', include('rosetta.urls_api')),
        )

Note: you need to enable some settings.

To uninstall Rosetta, simply comment out or remove the ``'rosetta'`` line in your ``INSTALLED_APPS``


Testing
-------

``pip install tox && tox``


Security
--------

Because Rosetta requires write access to some of the files in your Django project, access to the application is restricted to the administrator user only (as defined in your project's Admin interface)

If you wish to grant editing access to other users:

1. Create a `'translators'` group in your admin interface
2. Add the user you wish to grant translating rights to this group
