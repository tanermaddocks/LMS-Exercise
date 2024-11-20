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
        stmt = db.select(Teacher).filter_by(department=department).order_by(Teacher.id)
    else:
        stmt = db.select(Teacher).order_by(Teacher.id)
    return teachers_schema.dump(db.session.scalars(stmt))

# Read one - /teachers/id - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    teacher = db.session.scalar(db.select(Teacher).filter_by(id=teacher_id))
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} doesn't exist"}, 404

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
        
# Delete - /teachers/id - DELETE
@teachers_bp.route("/<int:teacher_id>", methods=["DELETE"])
def delete_teacher(teacher_id):
    teacher = db.session.scalar(db.select(Teacher).filter_by(id=teacher_id))
    if teacher:
        db.session.delete(teacher)
        db.session.commit()
        return {"message": f"Teacher '{teacher.name}' deleted successfully"}
    else:
        return {"message": f"Teacher with id {teacher_id} doesn't exist"}, 404

# Update - /teachers/id - PUT, PATCH

@teachers_bp.route("/<int:teacher_id>", methods=["PUT", "PATCH"])
def update_teacher(teacher_id):
    # find teacher
    teacher = db.session.scalar(db.select(Teacher).filter_by(id=teacher_id))
    # get data for update
    body_data = request.get_json()
    # if teacher exists
    if teacher:
        # update attributes
        teacher.name = body_data.get("name") or teacher.name
        teacher.department = body_data.get("department") or teacher.department
        teacher.address = body_data.get("address") or teacher.address
        # commit
        db.session.commit()
        # return success
        return teacher_schema.dump(teacher)
    # else return fail
    else:
        return {"message": f"Teacher with id {teacher_id} doesn't exist"}, 404