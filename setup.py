from setuptools import setup, find_packages

setup(
    name='pubsub.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.2.1',
    description='Python PubSub Adapter for gcloud',
    url='https://github.com/Superbalist/python-pubsub',
    install_requires=[
        'google-cloud-pubsub',
        'jsonschema',
    ],
    packages=find_packages(),
    zip_safe=False)
