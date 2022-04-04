from setuptools import setup
setup(
    name = 'dumaos-jsonrpc-client',
    version = '0.1.0',
    packages = ['dumarpc'],
    entry_points = {
        'console_scripts': [
            'dumarpc = cli.__main__:main'
        ]
    })