from flask import Blueprint, jsonify, request

from flaskr.common import get_order_from_arg, service_response as response
from flaskr.db import db_session
from flaskr.models import Server, Rack, ServerStatuses

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
        return response('server not exist', status=404)

    return jsonify(server.as_dict())


@bp.route('/create', methods=('POST',))
def create_server():
    server = Server.from_json(request.json)
    if not server:
        return response('bad json', status=400)
    target_rack = Rack.query.get(server.rack_id)
    if not target_rack:
        return response('target rack not exist', status=400)
    if target_rack.size >= target_rack.capacity.value:
        return response('rack is full', status=400)
    db_session.add(server)
    target_rack.increase_size()
    db_session.commit()
    return jsonify({'id': server.id})


@bp.route('/update/<int:id>', methods=('POST',))
def update_server(id):
    server = Server.query.get(id)
    if not server:
        return response(f'server with id: {id} does not exist', status=404)

    if server.status == ServerStatuses.deleted:
        return response('server already deleted. aborting.', status=400)

    content = request.json
    if not content or not isinstance(content, dict):
        return response('not changed')

    if not len(content):
        return response('got no args', status=400)

    if len(content) > 1:
        return response('update accept only 1 arg', status=400)

    valid_args = ('rack_id', 'status')
    if not any(arg in content for arg in valid_args):
        return response(f'got unknown arg. arg should be one of this: {valid_args}', status=400)

    # moving server to another rack
    if 'rack_id' in content:
        rack_id = content['rack_id']
        if not isinstance(rack_id, int):
            return response('rack_id must be integer', status=400)
        target_rack = Rack.query.get(rack_id)
        if not target_rack:
            return response(f'rack with id: {rack_id} does not exist', status=400)
        if target_rack.size >= target_rack.capacity.value:
            return response('rack is full', status=400)
        source_rack = Rack.query.get(server.rack_id)
        source_rack.decrease_size()
        target_rack.increase_size()
        server.rack = target_rack
        db_session.commit()
        return response('ok')

    # TODO changing server status
    return response('ok')
