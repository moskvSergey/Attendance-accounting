from flask import Blueprint, jsonify, request

from data import db_session
from data.groups import Groups

blueprint = Blueprint('group_api', __name__,
                      template_folder='templates')


@blueprint.route('/api/groups')
def get_news():
    session = db_session.create_session()
    groups = session.query(Groups).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only='name')
                 for item in groups]
        }
    )


@blueprint.route('/api/groups/<int:groups_id>', methods=['GET'])
def get_one_news(groups_id):
    session = db_session.create_session()
    groups = session.query(Groups).get(groups_id)
    if not groups:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': groups.to_dict(only='name')
        }
    )


@blueprint.route('/api/groups', methods=['POST'])
def create_groups():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    groups = Groups(
        name=request.json['name'],
    )
    session.add(groups)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/groups/<int:groups_id>', methods=['DELETE'])
def delete_groups(groups_id):
    session = db_session.create_session()
    groups = session.query(Groups).get(groups_id)
    if not groups:
        return jsonify({'error': 'Not found'})
    session.delete(groups)
    session.commit()
    return jsonify({'success': 'OK'})
