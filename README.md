# pyfox
Shell for Foxtrot

[![Build Status](https://travis-ci.org/gabber12/pyfox.svg?branch=master)](https://travis-ci.org/gabber12/pyfox) [![PyPI version](https://badge.fury.io/py/pyfox.svg)](https://badge.fury.io/py/pyfox)


## Installation
```sh
pip install pyfox --ignore-installed six
```

## Usage
#### Shell

```sh
$ foxtrot --help
Usage: commands.py [OPTIONS] HOST

  Use FQL to query foxtrot

  Options:
    --evaluate TEXT  Query to be evaluated
      --help           Show this message and exit.

foxtrot <endpoint>
> select * from analytics_event
Ctrl-D to exit or type exit
```

#### Client

```python
from pyfox import Foxtrot
client = Foxtrot(host)
result = client.select("select * from test_db")
for event in result.rows():
    print event['id']
```


