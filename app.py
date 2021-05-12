from routes import *
import config

app = config.app

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)