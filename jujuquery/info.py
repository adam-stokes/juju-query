# Copyright (c) 2015 Adam Stokes <adam.stokes@ubuntu.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Info interface
"""

from theblues.charmstore import CharmStore
from theblues.errors import EntityNotFound
import argparse
import sys
import textwrap


class InfoError(Exception):
    """ Problem with query
    """
    pass


class Info:
    def __init__(self):
        self.cs = CharmStore('https://api.jujucharms.com/v4')
        self.result = None

    def get(self, charm):
        """ Returns single entry for charm
        """
        try:
            if charm.startswith('cs:'):
                charm = charm[3:]
            self.result = self.cs.charm(charm)
        except EntityNotFound as e:
            raise InfoError(e)

    def render(self):
        """ Renders charm info

        Example:

        juju info cs:~adam-stokes/trusty/ghost-6

        Description
          A charm description

        Readme
          Blah blah

        """
        if not self.result:
            raise InfoError(
                "Must search for a charm before attempting to render it.")

        _id = self.result['Id']
        name = self.result['Meta']['charm-metadata']['Name']
        if _id.startswith('cs:'):
            _id = _id[3:]
        readme = self.cs.entity_readme_content(_id)
        try:
            description = self.result['Meta']['charm-metadata']['Description']
        except KeyError:
            raise InfoError("Only charms support the info method.")

        print(name)
        print("")
        print(textwrap.wrap(description.strip(), width=79).pop())
        print("")
        print("README")
        print("")
        print(readme)
        print("")


def parse_options(argv):
    parser = argparse.ArgumentParser(
        description='Juju info interface to charmstore',
        prog='juju-info')

    parser.add_argument('charm')
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    q = Info()
    q.get(opts.charm)
    q.render()
