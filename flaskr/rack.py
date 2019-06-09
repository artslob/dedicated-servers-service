from flask import Blueprint, jsonify

from flaskr.common import get_order_from_arg, service_response as response
from flaskr.models import Rack

bp = Blueprint('rack', __name__, url_prefix='/rack')


@bp.route('/all', methods=('GET',))
def all_racks():
    order = get_order_from_arg(Rack)
    rows = Rack.query.order_by(order).all()
    return jsonify([rack.as_dict() for rack in rows])


@bp.route('/<int:id>', methods=('GET',))
def get_rack(id):
    rack = Rack.query.get(id)
    if not rack:
        return response(f'rack id: {id} doest not exist', status=404)

    return jsonify(rack.as_dict())
