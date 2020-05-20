from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.sql_alchemy_repository import SqlAlchemyRepository
from src.data.orm import start_mappers
from src.domain import errors
from src.domain.service import copy_profile


connecting_string = f'mysql+mysqldb://root:sekret@127.0.0.1:52000/lunch_and_learn'

start_mappers()

engine = create_engine(connecting_string, echo=False)

Session = sessionmaker(bind=create_engine())
app = Flask(__name__)


@app.route("/clone_profile", methods=['POST'])
def clone_profile_endpoint():
    try:
        session = Session()
        repository = SqlAlchemyRepository()

        profile = repository.get(request.json['profile_id'])

        copied_profile = copy_profile(profile)

        repository.add(copied_profile)
        session.commit()

    except (errors.CloningProfileWithRecurringExpenses, errors.CloningProfileWithRecurringTimeEntries) as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'profile_id': copied_profile.id}), 201
