from flask import Flask, jsonify, request

from src.domain import errors
from src.service_layer import services
from src.service_layer.unit_of_work import SqlAlchemyUnitOfWork

app = Flask(__name__)


@app.route("/clone_profile", methods=['POST'])
def clone_profile_endpoint():
    try:
        profile_id = services.copy_profile(request.json['profile_id'], SqlAlchemyUnitOfWork())
    except (errors.CloningProfileWithRecurringExpenses, errors.CloningProfileWithRecurringTimeEntries) as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'profile_id': profile_id.id}), 201
