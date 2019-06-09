from flask import request, jsonify


def get_order_from_arg(model, sort_arg='sort'):
    arg = request.args.get(sort_arg, '')
    if arg == 'created':
        order = model.created
    elif arg == 'changed':
        order = model.changed
    else:
        order = model.id
    return order


def service_response(message: str, *, status=200):
    return jsonify({'status': message}), status
