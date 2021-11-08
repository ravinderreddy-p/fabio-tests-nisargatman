from flask import jsonify
from wikiapp import app


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status_code': 404,
        'message': 'Page not found'
    }), 404


@app.errorhandler(410)
def not_found(error):
    return jsonify({
        'status_code': 410,
        'message': 'Area exceeds the limit'
    }), 410


@app.errorhandler(411)
def not_found(error):
    return jsonify({
        'status_code': 411,
        'message': 'Population exceeds the limit'
    }), 411


@app.errorhandler(502)
def not_found(error):
    return jsonify({
        'status_code': 502,
        'message': 'Internal Server Error'
    }), 502