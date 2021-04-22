from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AI Connector',
    url='https://gitlab.com/natix/visiondeploy/aiconnector',
    author='Guja',
    author_email='guja@natix.io',
    # Needed to actually package something
    packages=['ai_connector'],
    # Needed for dependencies
    install_requires=['grpcio', 'grpcio-tools'],
    # *strongly* suggested for sharing
    version='0.1',
)
