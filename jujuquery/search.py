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

""" Search interface
"""

from theblues.charmstore import CharmStore
from theblues.errors import EntityNotFound
import argparse
import sys


class QueryError(Exception):
    """ Problem with query
    """
    pass


class Query:
    def __init__(self):
        self.cs = CharmStore('https://api.jujucharms.com/v4')
        self.charm = None

    @property
    def _is_fuzzy(self):
        """ Checks if the charm argument contains * or any other
        indication that it's a fuzzy search.
        """
        if ['*', '?', '.'] in self.charm:
            return True
        return False

    def search(self, charm):
        """ Searches for charm

        Arguments:
        charm: name of service
        """
        try:
            self.charm = self.cs.search(self.charm)
        except EntityNotFound as e:
            raise QueryError(e)

    def get(self, charm):
        """ Returns single entry for charm
        """
        try:
            self.charm = self.cs.charm(charm)
        except EntityNotFound as e:
            raise QueryError(e)

    def render(self):
        """ Renders charm results
        """
        if not self.charm:
            raise QueryError(
                "Must search for a charm before attempting to render it.")
        meta = self.charm['Meta']['charm-metadata']
        stat = self.charm['Meta']['stats']
        name = meta['Name']
        dl = stat['ArchiveDownloadCount']
        summary = meta['Summary']
        print("{} {} Summary".format("Charm".ljust(len(name)),
                                     "D/L".ljust(len(name))))
        print("{} {} {}".format(name.ljust(len(name)),
                                str(dl).ljust(len(name)),
                                summary))


def parse_options(argv):
    parser = argparse.ArgumentParser(
        description='Juju search interface to charmstore',
        prog='juju-search')

    parser.add_argument('charm')
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    q = Query()
    q.get(opts.charm)
    q.render()
