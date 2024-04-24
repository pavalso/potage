# pypotage

[![img](https://img.shields.io/pypi/v/pypotage.svg)](https://pypi.org/project/pypotage/)
[![img](https://img.shields.io/pypi/pyversions/pypotage.svg)](https://pypi.org/project/pypotage/)
![example workflow](https://github.com/pavalso/potage/actions/workflows/python-package.yml/badge.svg)
TODO - Add coverage badge

A simple Python package that provides an easy way to use Dependency Injection in your projects.

![alt text](https://imgur.com/7eK0mHJ.png)

## Key Features

- Easy to use
- Supports both function and class-based dependency 
injection
- Allows customizing the way dependencies are resolved
- Allows for the use of custom containers

## Installing

To install the latest **pypotage** version, run the following command:
````bash
$ python3 -m pip install -U pypotage
````

#### Development

To install the development version:
````bash
$ git clone https://github.com/pavalso/potage.git
$ cd potage
$ git checkout development
$ python3 -m pip install -U .
````

## Quick Examples

#### Basic usage
````python
import pypotage
import logging

@pypotage.prepare
def logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(__name__)

pypotage.cook(logging.Logger).take_out().info("Hello World!")
````

#### Using classes
````python
import pypotage

class A:
    def __init__(self):
        ...

@pypotage.prepare
class B(A):
    def __init__(self):
        ...

pypotage.cook(A).take_out()  # returns an instance of B
````
