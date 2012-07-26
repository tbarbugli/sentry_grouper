from setuptools import setup, find_packages
from sentry_grouper import VERSION

setup(
    name='sentry_grouper',
    version=VERSION,
    author='Tommaso Barbugli',
    author_email='tbarbugli@gmail.com',
    url='http://github.com/tbarbugli/sentry_grouper',
    description='A plugin to create custom groupers',
    long_description='',
    packages=find_packages(),
    install_requires=['sentry'],
    test_suite='runtests.runtests',
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
