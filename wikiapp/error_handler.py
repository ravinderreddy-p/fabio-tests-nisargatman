from flask import jsonify

from wikiapp import app


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status_code": 404,
        # "error": error,
        "message": "Page not found"
    }), 404