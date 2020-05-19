import app as app
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.sql_alchemy_repository import SqlAlchemyRepository
from src.data.orm import start_mappers
from src.domain import errors
from src.service_layer import services

connecting_string = f'mysql+mysqldb://root:sekret@127.0.0.1:52000/lunch_and_learn'

start_mappers()

engine = create_engine(connecting_string, echo=False)

Session = sessionmaker(bind=create_engine())
app = Flask(__name__)


@app.route("/clone_profile", methods=['POST'])
def clone_profile_endpoint():
    try:
        profile_id = services.copy_profile(request.json['profile_id'], SqlAlchemyRepository(), Session())
    except (errors.CloningProfileWithRecurringExpenses, errors.CloningProfileWithRecurringTimeEntries) as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'profile_id': profile_id.id}), 201
