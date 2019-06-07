from flask import Blueprint
from flask import jsonify

from flaskr.common import get_order_from_arg
from flaskr.models import Server

bp = Blueprint('server', __name__, url_prefix='/server')


@bp.route('/all', methods=('GET',))
def all_servers():
    order = get_order_from_arg(Server)
    rows = Server.query.order_by(order).all()
    return jsonify([server.as_dict() for server in rows])


@bp.route('/<int:id>', methods=('GET',))
def get_rack(id):
    server = Server.query.get(id)
    if not server:
        return jsonify({}), 404

    return jsonify(server.as_dict())
