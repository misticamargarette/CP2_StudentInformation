from flask import Flask

from controllers.web_controller import create_web_controller


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "student-information-local-secret"
    app.register_blueprint(create_web_controller())
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
