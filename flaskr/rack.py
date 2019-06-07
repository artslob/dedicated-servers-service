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
