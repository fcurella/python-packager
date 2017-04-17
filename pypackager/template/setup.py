import os
from setuptools import setup, find_packages


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('REQUIREMENTS').splitlines()
tests_requirements = read('REQUIREMENTS-TESTS').splitlines()

setup(
    name="{{ package_name }}",
    version="0.0.1",
    description="",
    long_description=read('README.rst'),
    url='',
    license='{{ license.name }}',
    author='{{ author.name }}',
    author_email='{{ author.email }}',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',{{#license}}
        '{{ classifier }}',{{/license}}
        'Programming Language :: Python',
    ],
    install_requires=requirements,
    tests_require=tests_requirements,
)
