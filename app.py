from flask import Flask, redirect, request
from urllib2 import urlopen
from re import findall

app = Flask(__name__)

GITHUB_URL = ('https://github.com/luanfonceca/'
              'waffle2shields#waffleio-to-shieldsio')
WAFFLE_URL = 'https://badge.waffle.io/{user}/{repo}.png?label={label}'
SHIELDS_URL = ('http://img.shields.io/badge/'
               '{subject}-{status}-{color}.svg?style={style}')


@app.route("/")
def parse_badges():
    data = request.args.to_dict()

    if not data:
        return redirect(GITHUB_URL)

    html = urlopen(WAFFLE_URL.format(**data)).read()
    shields_data = {
        'subject': data.get('label', 'Waffle').title(),
        'status': findall(r'<text.*?>(.*?)</text>', html)[-1],
        'color': findall(r'<rect.*? fill="#?([^\s^"]+)', html)[2],
        'style': data.get('style')
    }
    return redirect(SHIELDS_URL.format(**shields_data))


if __name__ == "__main__":
    app.run(debug=True)
