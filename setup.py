from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AI Connector',
    url='https://gitlab.com/natix/visiondeploy/aiconnector',
    author='Guja',
    author_email='guja@natix.io',
    # Needed to actually package something
    packages=['ai_connector','ai_connector/client', 'ai_connector/utils'],
    # Needed for dependencies
    install_requires=['grpcio'],
    # *strongly* suggested for sharing
    version='1.0',
)
