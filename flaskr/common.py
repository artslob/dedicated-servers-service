from flask import request


def get_order_from_arg(model, sort_arg='sort'):
    arg = request.args.get(sort_arg, '')
    if arg == 'created':
        order = model.created
    elif arg == 'changed':
        order = model.changed
    else:
        order = model.id
    return order
