from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.enrolment import Enrolment, enrolments_schema, enrolment_schema

enrolments_bp = Blueprint("enrolments", __name__, url_prefix="/enrolments")


# Read all
@enrolments_bp.route("/")
def get_enrolments():
    stmt = db.select(Enrolment)
    enrolments_list = db.session.scalars(stmt)
    return enrolments_schema.dump(enrolments_list)

# Read one
@enrolments_bp.route("/<int:enrolment_id>")
def get_enrolment(enrolment_id):
    stmt = db.select(Enrolment).filter_by(id=enrolment_id)
    enrolment = db.session.scalar(stmt)
    if enrolment:
        return enrolment_schema.dump(enrolment)
    else:
        return {"message": f"Enrolment with id {enrolment_id} does not exist"}, 404
    
# Create
@enrolments_bp.route("/", methods=["POST"])
def create_enrolment():
    try:
        # get the data from the request body
        body_data = request.get_json()
        # create a Enrolment instance
        enrolment = Enrolment(
            enrolment_date=body_data.get("enrolment_date"),
            student_id=body_data.get("student_id"),
            course_id=body_data.get("course_id")
        )
        # add to session and commit
        db.session.add(enrolment)
        db.session.commit()
        # return a response
        return enrolment_schema.dump(enrolment), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": err.orig.diag.message_detail}, 409
        
# Delete
@enrolments_bp.route("/<int:enrolment_id>", methods=["DELETE"])
def delete_enrolment(enrolment_id):
    enrolment = db.session.scalar(db.select(Enrolment).filter_by(id=enrolment_id))
    if enrolment:
        db.session.delete(enrolment)
        db.session.commit()
        return {"message": f"Student '{enrolment.student_id}' removed from course '{enrolment.course_id}'"}
    else:
        return {"message": f"Enrolment with id {enrolment_id} doesn't exist"}, 404
    
# Update
@enrolments_bp.route("/<int:enrolment_id>", methods=["PUT", "PATCH"])
def update_enrolment(enrolment_id):
    try:
        stmt = db.select(Enrolment).filter_by(id=enrolment_id)
        enrolment = db.session.scalar(stmt)
        body_data = request.get_json()
        if enrolment:
            enrolment.enrolment_date = body_data.get("enrolment_date") or enrolment.enrolment_date
            enrolment.student_id = body_data.get("student_id") or enrolment.student_id
            enrolment.course_id = body_data.get("course_id") or enrolment.course_id
            db.session.commit()
            return enrolment_schema.dump(enrolment)
        else:
            return {"message": f"Enrolment with id {enrolment_id} does not exist"}
    except DataError as err:
        # for attr in dir(err.orig.diag):
        #     print("obj.%s = %r" % (attr, getattr(err.orig.diag, attr)))
        return {"message": err.orig.diag.message_primary}, 409