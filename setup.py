try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from rust_ext import (build_rust_cmdclass, develop_including_rust,
                      install_lib_including_rust)

config = {
    'description': 'Automatic rule based Linux Time Tracker',
    'author': 'Tautvidas Sipavicius',
    'author_email': 'flakas@tautvidas.com',
    'url': 'https://github.com/flakas/Latte',
    'install_requires': ['sqlalchemy', 'pysqlite'],
    'cmdclass': {
        'build_rust': build_rust_cmdclass('latte/x11_extension/Cargo.toml'),
        'install_lib': install_lib_including_rust,
        'develop': develop_including_rust,
    },
    'zip_safe': False,
    'packages': ['latte'],
    'scripts': ['bin/latte', 'bin/lattestats'],
    'version': '3.0',
    'name': 'latte'
}

setup(**config)
