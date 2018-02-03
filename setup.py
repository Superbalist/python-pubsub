from setuptools import setup, find_packages

setup(
    name='pubsub.py',
    author='Superbalist Engineering',
    author_email='tech@superbalist.com',
    version='0.3.5',
    description='Python PubSub Adapter for gcloud',
    url='https://github.com/Superbalist/python-pubsub',
    install_requires=[
        'google.cloud.pubsub==0.29.0',
        'jsonschema',
        'requests',
    ],
    packages=find_packages(),
    zip_safe=False)
