import os
from setuptools import setup, find_packages


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''


requirements = read('REQUIREMENTS').splitlines()
tests_requirements = read('TEST-REQUIREMENTS').splitlines()

os.environ["PYTHONDONTWRITEBYTECODE"] = 'true'

setup(
    name="python-packager",
    version="0.0.5",
    description="A command-line tool to create Python Packages.",
    long_description=read('README.rst'),
    url='https://github.com/fcurella/python-packager',
    license='MIT',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    scripts=['bin/pypackager'],
    install_requires=requirements,
    tests_require=tests_requirements,
)
