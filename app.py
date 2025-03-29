from gevent import monkey
monkey.patch_all()

from app import create_app
from app import routes

app = create_app()
app.register_blueprint(routes.routes)



if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer

    http_server = WSGIServer(("0.0.0.0", 5000), app)
    http_server.serve_forever()
    app.run(debug=True)