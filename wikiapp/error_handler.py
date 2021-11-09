from flask import jsonify
from wikiapp import app


@app.errorhandler(400)
def not_found(error):
    return jsonify({
        'status_code': 400,
        'message': 'Bad Request'
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status_code': 404,
        'message': 'Page or resource not found'
    }), 404


@app.errorhandler(502)
def not_found(error):
    return jsonify({
        'status_code': 502,
        'message': 'Internal Server Error'
    }), 502