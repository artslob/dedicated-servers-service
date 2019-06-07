from flask import Blueprint
from flask import jsonify

from flaskr.models import Rack

bp = Blueprint('rack', __name__, url_prefix='/rack')


@bp.route('/all', methods=('GET',))
def all_racks():
    rows = Rack.query.all()
    columns = ('id', 'created', 'changed', 'size', 'capacity')
    result = [{name: getattr(rack, name, '<empty>') for name in columns} for rack in rows]
    return jsonify(result)


@bp.route('/<int:id>', methods=('GET',))
def get_rack(id):
    rack = Rack.query.get(id)
    if not rack:
        return jsonify({}), 404

    # TODO make rack and server json-serializable
    columns = ('id', 'created', 'changed', 'size', 'capacity')
    return jsonify({name: getattr(rack, name, '<empty>') for name in columns})
