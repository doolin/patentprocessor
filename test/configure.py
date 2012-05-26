#!/usr/bin/env python

import yaml
stream = file('test.yaml','r')
configuration = yaml.load(stream)

print configuration
print configuration['filepath']
print configuration['regex']
