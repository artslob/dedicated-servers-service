from flask import Blueprint, jsonify, request

from flaskr.common import get_order_from_arg
from flaskr.db import db_session
from flaskr.models import Server, Rack

bp = Blueprint('server', __name__, url_prefix='/server')


@bp.route('/all', methods=('GET',))
def all_servers():
    order = get_order_from_arg(Server)
    rows = Server.query.order_by(order).all()
    return jsonify([server.as_dict() for server in rows])


@bp.route('/<int:id>', methods=('GET',))
def get_server(id):
    server = Server.query.get(id)
    if not server:
        return jsonify({}), 404

    return jsonify(server.as_dict())


@bp.route('/create', methods=('POST',))
def create_server():
    server = Server.from_json(request.json)
    if not server:
        return jsonify({'status': 'bad json'}), 400
    target_rack = Rack.query.get(server.rack_id)
    if not target_rack:
        return jsonify({'status': 'target rack not exist'}), 400
    if target_rack.size >= target_rack.capacity.value:
        return jsonify({'status': 'rack is full'}), 400
    db_session.add(server)
    target_rack.size = Rack.size + 1
    db_session.commit()
    return jsonify({'id': server.id})
