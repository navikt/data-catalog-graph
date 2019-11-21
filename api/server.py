from flask import redirect, render_template

import config

connex_app = config.connex_app
connex_app.add_api("swagger.yml")

@connex_app.route("/")
def swagger():
    return '/api/ui'

if __name__ == "__main__":
    connex_app.run(debug=True)