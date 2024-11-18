from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import db
from models.teacher import Teacher, teachers_schema, teacher_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# Create - /teachers - POST
# Read all - /teachers - GET
# Read one - /teachers/id - GET
# Update - /teachers/id - PUT, PATCH
# Delete - /teachers/id - DELETE


# Read all - /teachers - GET
# Read all from a single department - /teachers?department=__ - GET
@teachers_bp.route("/")
def get_teachers():
    department = request.args.get("department")
    if department:
        stmt = db.select(Teacher).filter_by(department=department)
    else:
        stmt = db.select(Teacher)
    return teachers_schema.dump(db.session.scalars(stmt))

# Read one - /teachers/id - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    teacher = db.session.scalar(db.select(Teacher).filter_by(id=teacher_id))
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not "
                "exist"}, 404

# Create - /teachers - POST
@teachers_bp.route("/", methods=["POST"]) 
def create_teacher():
    try:
        body_data = request.get_json()
        new_teacher = Teacher(
            name=body_data.get("name"),
            department=body_data.get("department"),
            address=body_data.get("address")
        )
        db.session.add(new_teacher)
        db.session.commit()
        return teacher_schema.dump(new_teacher), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' "
                    "is required"}, 409