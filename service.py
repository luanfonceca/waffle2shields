from urllib2 import urlopen
from re import findall


class Service(object):
    shields_url = ('http://img.shields.io/badge/'
                   '{0.subject}-{0.status}-{0.color}.svg?style={0.style}')

    def __init__(self, **kw):
        self.data = kw
        self.html = urlopen(self.service_url.format(**self.data)).read()

    def get_shields_url(self):
        return self.shields_url.format(self)

    @property
    def subject(self):
        return self.data.get('label')

    @property
    def style(self):
        return self.data.get('style')

    @property
    def service_url(self):
        raise NotImplementedError

    @property
    def color(self):
        raise NotImplementedError

    @property
    def status(self):
        raise NotImplementedError


class Waffle(Service):
    @property
    def service_url(self):
        return 'https://badge.waffle.io/{user}/{repo}.png?label={label}'

    @property
    def color(self):
        return findall(r'<rect.*? fill="#?([^\s^"]+)', self.html)[2]

    @property
    def status(self):
        return findall(r'<text.*?>(.*?)</text>', self.html)[-1]


class Landscape(Service):
    @property
    def service_url(self):
        return ('https://landscape.io/github/'
                '{user}/{repo}/{branch}/landscape.png')

    @property
    def color(self):
        hex = findall(r'<rect.*? fill="#?([^\s^"]+)', self.html)[1]
        if len(hex) == 3:
            return '{0}{0}{1}{1}{2}{2}'.format(*list(hex))
        return hex

    @property
    def status(self):
        return findall(r'<text.*?>(.*?)</text>', self.html)[-1]
