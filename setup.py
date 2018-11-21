from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pubsub.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.3.10',
    description='Python PubSub Adapter for gcloud',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Superbalist/python-pubsub',
    install_requires=[
        'google.cloud.pubsub==0.33.1',
        'jsonschema',
        'requests',
    ],
    packages=find_packages(),
    zip_safe=False)
