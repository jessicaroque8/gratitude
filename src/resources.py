# modules
from flask import request, jsonify, json, wrappers
from flask_restful import abort, Api, Resource
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest
# local
from models import db, Entry, entry_schema, entries_schema
from exceptions import GratitudeError, NotFoundError, ValidationError, BadReqError

api = Api()
gratitude_error = GratitudeError()
invalid_json_error = BadReqError('Invalid JSON.')


def get_entry(entry_id):
    try:
        entry = Entry.query.filter_by(id=entry_id).one()
        return [entry, None]
    except NoResultFound:
        err_obj = NotFoundError('entry', entry_id).get()
        return [None, err_obj]
    except Exception:
        err_obj = gratitude_error.get()['error']
        return [None, err_obj]


def handle_response(obj, status_code):
    if type(obj) is wrappers.Response:
        response = obj
    else:
        response = jsonify(obj)

    response.status_code = status_code
    return response


class EntryItem(Resource):

    def get(self, entry_id):
        try:
            data, error = get_entry(entry_id)
            if error:
                return handle_response(error, 404)
            else:
                return handle_response(entry_schema.jsonify(data), 200)
        except Exception as err:
            print(err)
            return handle_response(gratitude_error.get(), 422)

    def put(self, entry_id):
        try:
            data, error = get_entry(entry_id)
            if error:
                return handle_response(error, 404)
            else:
                if not request.is_json:
                    raise invalid_json_error
                else:
                    request_body = request.get_json(force=True)
                    if request_body.get('title'):
                        data.title = request_body['title']
                    if request_body.get('body'):
                        data.body = request_body['body']
                    db.session.commit()
                    db.session.refresh(data)
                    return handle_response(entry_schema.jsonify(data), 201)
        except BadReqError as err:
            return handle_response(err.get(), 400)
        except BadRequest as err:
            return handle_response(invalid_json_error.get(), 400)
        except Exception as err:
            print(err)
            return handle_response(gratitude_error.get(), 422)

    def delete(self, entry_id):
        try:
            data, error = get_entry(entry_id)
            if error:
                return handle_response(error, 404)
            else:
                db.session.delete(data)
                db.session.commit()
                return '', 204
        except Exception as err:
            print(err)
            return handle_response(gratitude_error.get(), 400)


# shows a list of all entries, and lets you POST to add a new entry
class EntryList(Resource):
    def get(self):
        try:
            entries = Entry.query.all()
            return handle_response(entries_schema.jsonify(entries), 200)
        except Exception as err:
            print(err)
            return handle_response(gratitude_error.get(), 422)

    def post(self):
        try:
            data, error = entry_schema.load(
                request.get_json(force=True)
            )
            if error:
                raise ValidationError(error)
            else:
                new_entry = Entry(title=data.title, body=data.body)
                db.session.add(new_entry)
                db.session.commit()
                db.session.refresh(new_entry)
                return handle_response(entry_schema.jsonify(new_entry), 201)
        except ValidationError as err:
            return handle_response(err.get(), 400)
        except Exception as err:
            print(err)
            return handle_response(gratitude_error.get(), 422)


# setup the Api resource routing here
api.add_resource(EntryList, '/entries')
api.add_resource(EntryItem, '/entries/<entry_id>')
