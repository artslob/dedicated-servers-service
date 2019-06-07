from flask import Blueprint
from flask import jsonify

from flaskr.models import Server

bp = Blueprint('server', __name__, url_prefix='/server')


@bp.route('/all', methods=('GET',))
def all_servers():
    rows = Server.query.all()
    columns = ('id', 'created', 'changed', 'rack_id')
    result = [{name: getattr(rack, name, '<empty>') for name in columns} for rack in rows]
    return jsonify(result)
