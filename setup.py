#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-admin-overlay',
    version='.'.join(map(str, __import__('admin_overlay').VERSION)),
    license='Apache License, Version 2.0',

    install_requires=[],
    dependency_links=[],

    description='Django admin-overlay - present the admin user an overlay at the frontend website pages',
    long_description=open('README.rst').read(),

    author='Diederik van der Boor',
    author_email='vdboor@edoburu.nl',

    url='https://github.com/edoburu/django-admin-overlay',
    download_url='https://github.com/edoburu/django-admin-overlay/zipball/master',

    packages=find_packages(),
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
