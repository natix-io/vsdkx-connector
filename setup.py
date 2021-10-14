from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='vsdkx-connector',
    url='https://github.com/natix-io/vsdkx-connector.git',
    author='Guja',
    author_email='g.mekokishvili@omedia.ge',
    # Needed to actually package something
    packages=['connector','connector/client', 'connector/utils'],
    # Needed for dependencies
    install_requires=['grpcio'],
    # *strongly* suggested for sharing
    version='2.0',
)
