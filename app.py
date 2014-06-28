from flask import Flask, redirect, request

from service import Waffle, Landscape

GITHUB_URL = ('https://github.com/luanfonceca/'
              'waffle2shields#waffleio-to-shieldsio')

app = Flask(__name__)


@app.route("/<string:service_slug>/")
def parse_badges(service_slug):
    data = request.args.to_dict()
    service = None
    if service_slug == 'waffle':
        service = Waffle(**data)
    elif service_slug == 'landscape':
        service = Landscape(**data)
    else:
        return redirect(GITHUB_URL)
    return redirect(service.get_shields_url())


if __name__ == "__main__":
    app.run(debug=True)
