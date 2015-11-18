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
        self.charm_search = None
        self.result = None

    @classmethod
    def is_fuzzy(cls, charm):
        glob_chars = set('~*')
        if any((c in glob_chars) for c in charm):
            return True
        return False

    @classmethod
    def valid_filter(cls, charm):
        fail_glob_chars = set('.?[]')
        if any((c in fail_glob_chars) for c in charm):
            return False
        return True

    def _save_charm_search(self, charm):
        """ Saves the charm search query, sanitizing any wildcards
        """
        charm = charm.translate({ord(i): None for i in '~*'})
        self.charm_search = charm

    def filter_non_name_matches(self, result):
        """ The search query doesnt return just results with charm_search
        in the name, so we filter that out
        """
        self.result = [item for item in result
                       if self.charm_search in item['Id']]

    def search(self, charm, promulgated=True):
        """ Searches for charm

        Eg:
        https://api.jujucharms.com/charmstore/v4/search?text=nova&autocomplete=1&limit=100

        Only blessed ones:
        https://api.jujucharms.com/charmstore/v4/search?text=nova&autocomplete=1&limit=100&owner=
        Arguments:
        charm: name of service
        """
        try:
            self._save_charm_search(charm)
            self.result = self.cs.search(charm,
                                         autocomplete=True,
                                         promulgated_only=promulgated,
                                         limit=25)
        except EntityNotFound as e:
            raise QueryError(e)

    def get(self, charm):
        """ Returns single entry for charm
        """
        try:
            self._save_charm_search(charm)
            self.result = dict(Id=self.cs.entityId(charm))
        except EntityNotFound as e:
            raise QueryError(e)

    def render(self):
        """ Renders charm results

        Example:

        juju search nova

        Trusty
          nova-cloud-controller
          nova-compute

        Precise
          nova-compute

        User contributed
          nova-compute-vmware
        """
        if not self.result:
            raise QueryError(
                "Must search for a charm before attempting to render it.")

        if not isinstance(self.result, list):
            self.result = [self.result]

        series_map = {
            'trusty': [],
            'precise': [],
            'namespaced': [],
        }

        self.filter_non_name_matches(self.result)
        for entity in self.result:
            _id = entity['Id']
            item = _id
            if entity['Id'].startswith('cs:'):
                item = entity['Id'][3:]
            charm = self.cs.entity(item)
            try:
                meta = charm['Meta']['charm-metadata']
            except KeyError:
                # Probably a bundle
                continue
            stat = charm['Meta']['stats']
            dl = stat['ArchiveDownloadCount']
            summary = meta['Summary']

            if Query.is_fuzzy(item):
                series_map['namespaced'].append(
                    (_id, dl, summary)
                )
            elif 'trusty' in item:
                series_map['trusty'].append(
                    (_id, dl, summary)
                )
            elif 'precise' in item:
                series_map['precise'].append(
                    (_id, dl, summary)
                )

        valid_series = None
        for series in sorted(series_map.keys(), reverse=True):
            if len(series_map[series]) == 0:
                continue
            valid_series = series
            print(series.capitalize())
            print("")
            for _id, dl, summary in series_map[series]:
                print(" {}".format(_id))
            print("")

        if valid_series:
            item = series_map[valid_series][0]
            print("Example:")
            print("")
            print(" juju deploy {}".format(item[0]))
            print("")
            print("Get additional information:")
            print("")
            print(" juju info {}".format(item[0]))
            print("")


def parse_options(argv):
    parser = argparse.ArgumentParser(
        description='Juju search interface to charmstore',
        prog='juju-search')

    parser.add_argument('charm')
    return parser.parse_args(argv)


def main():
    opts = parse_options(sys.argv[1:])

    q = Query()
    if not q.valid_filter(opts.charm):
        raise QueryError("Invalid filter found, only ~ and * are supported")

    if q.is_fuzzy(opts.charm):
        q.search(opts.charm, promulgated=False)
    else:
        try:
            q.get(opts.charm)
        except QueryError:
            # No filter passed but not a valid full name charm
            q.search(opts.charm, promulgated=False)

    q.render()
