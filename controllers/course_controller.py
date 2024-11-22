from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes

from init import db
from models.course import Course, courses_schema, course_schema

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


# Read all
@courses_bp.route("/")
def get_courses():
    stmt = db.select(Course)
    courses_list = db.session.scalars(stmt)
    return courses_schema.dump(courses_list)

# Read one
@courses_bp.route("/<int:course_id>")
def get_course(course_id):
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        return course_schema.dump(course)
    else:
        return {"message": f"Course with id {course_id} does not exist"}, 404
    
# Create
@courses_bp.route("/", methods=["POST"])
def create_course():
    try:
        # get the data from the request body
        body_data = request.get_json()
        # create a Course instance
        course = Course(
            name=body_data.get("name"),
            duration=body_data.get("duration"),
            teacher_id=body_data.get("teacher_id")
        )
        # add to session and commit
        db.session.add(course)
        db.session.commit()
        # return a response
        return course_schema.dump(course), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": "The name cannot be null"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Name must be unique"}, 409
        
# Delete
@courses_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = db.session.scalar(db.select(Course).filter_by(id=course_id))
    if course:
        db.session.delete(course)
        db.session.commit()
        return {"message": f"Course '{course.name}' deleted successfully"}
    else:
        return {"message": f"Course with id {course_id} doesn't exist"}, 404
    
# Update
@courses_bp.route("/<int:course_id>", methods=["PUT", "PATCH"])
def update_course(course_id):
    try:
        stmt = db.select(Course).filter_by(id=course_id)
        course = db.session.scalar(stmt)
        body_data = request.get_json()
        if course:
            course.name = body_data.get("name") or course.name
            course.duration = body_data.get("duration") or course.duration
            course.teacher_id = body_data.get("teacher_id") or course.teacher_id
            db.session.commit()
            return course_schema.dump(course)
        else:
            return {"message": f"Course with id {course_id} does not exist"}
    except IntegrityError:
        return {"message": "Name must be unique"}, 409
    except DataError as err:
        # for attr in dir(err.orig.diag):
        #     print("obj.%s = %r" % (attr, getattr(err.orig.diag, attr)))
        return {"message": err.orig.diag.message_primary}, 409