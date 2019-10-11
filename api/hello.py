import connexion


def post_greeting(name: str) -> str:
    return 'Hello {name}'.format(name=name)

if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='./openapi/')
    app.add_api('openapi.yaml', strict_validation=True, arguments={'title': 'Hello World Example'})
    app.run()