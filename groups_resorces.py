from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.groups import Groups


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)

def abort_if_groups_not_found(groups_id):
    session = db_session.create_session()
    groups = session.query(Groups).get(groups_id)
    if not groups:
        abort(404, message=f"News {groups_id} not found")

class GroupsResource(Resource):
    def get(self, groups_id):
        abort_if_groups_not_found(groups_id)
        session = db_session.create_session()
        groups = session.query(Groups).get(groups_id)
        return jsonify({'groups': groups.to_dict(
            only='name')})

    def delete(self, groups_id):
        abort_if_groups_not_found(groups_id)
        session = db_session.create_session()
        groups = session.query(Groups).get(groups_id)
        session.delete(groups)
        session.commit()
        return jsonify({'success': 'OK'})


class GroupsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groups = session.query(Groups).all()
        group = []
        for p in groups:
            a_dict = {"name": p.name}
            group.append(a_dict)
        print(type(groups))
        return jsonify({'groups': group})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        groups = Groups(
            name=args['name'],
        )
        session.add(groups)
        session.commit()
        return jsonify({'success': 'OK'})
