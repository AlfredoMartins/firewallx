from flask import Blueprint, jsonify
import utils

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/logs')
def get_logs():
    res = utils.read_logs()
    return jsonify(res)

@api.route('/blocked_ips/<id>', methods=['DELETE'])
def delete_blocked_ip(id):
    print("IP: ", id)
    firewall.allow(id)
    return 'Blocked IP Logs...'

# Custom requests
@api.before_request
def before_request():
    pass

@api.after_request
def after_request():
    pass

@api.teardown_request
def teardown_request():
    pass


# Error Handling
@api.errorhandler(404)
def page_not_found(e):
    return "Page not found :(", 404

@api.errorhandler(500)
def internal_server_error(e):
    return "Internal server error", 500

