from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/logs')
def get_logs():
    res = read_logs()
    return jsonify(res)

@api.route('/blocked_ips/<id>', methods=['DELETE'])
def delete_blocked_ip(id):
    print("IP: ", id)
    unblock_ip(id)
    return 'Blocked IP Logs...'