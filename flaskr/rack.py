from flask import Blueprint

from flaskr.db import get_db
from flask import jsonify

bp = Blueprint('rack', __name__, url_prefix='/rack')


@bp.route('/all', methods=('GET',))
def all_racks():
    db = get_db()
    rows = db.execute('SELECT id, created, changed, size, capacity FROM rack').fetchall()
    result = [{name: row[name] for name in ('id', 'created', 'changed', 'size', 'capacity')} for row in rows]
    return jsonify(result)
