from distutils.core import setup
setup(
    name = 'pyfox',
    packages = ['pyfox'],
    version = '0.15',
    description = 'Shell for foxtrot',
    author = 'Shubham Sharma',
    author_email = 'shubham.sha12@gmail.com',
    url = 'https://github.com/gabber12/pyfox',
    download_url = 'https://github.com/gabber12/pyfox/archive/0.15.tar.gz',
    keywords = ['shell', 'foxtrot', 'cli'],
    classifiers = [],
    entry_points = {
                    'console_scripts': ['foxtrot=pyfox.commands:main'],
    },
    install_requires=[
              'click',
              'json-logic',
              'requests',
              'prompt_toolkit',
              'pygments'
    ]
)
