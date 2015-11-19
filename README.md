# juju-query
> Plugin to query charmstore

This plugin allows you to search the charmstore from cli and get additional
information about a charm (ie. README, charm location)


# installation

via APT:
```
$ sudo apt-add-repository ppa:adam-stokes/juju-query
$ sudo apt-get update
$ sudo apt-get install juju-query
```

via pip:
```
$ pip install juju-query
```
> Make sure juju-search can be located in your $PATH

# usage

```
$ juju search ghost
$ juju info cs:~adam-stokes/trusty/ghost-6
```

# todo

- [ ] get config options for charm
- [ ] expose relations provided/required
- [ ] add limiting
- [ ] bundle search support

# license

The MIT License (MIT)

Copyright (c) 2015 Adam Stokes <adam.stokes@ubuntu.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

