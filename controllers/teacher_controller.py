from flask import Blueprint, request

from init import db
from models.teacher import Teacher, teachers_schema, teacher_schema

teachers_bp = Blueprint("teachers", __name__, url_prefix="/teachers")

# Create - /teachers - POST
# Read all - /teachers - GET
# Read one - /teachers/id - GET
# Update - /teachers/id - PUT, PATCH
# Delete - /teachers/id - DELETE


# Read all - /teachers - GET
@teachers_bp.route("/")
def get_teachers():
    return teachers_schema.dump(db.session.scalars(db.select(Teacher)))

# Read one - /teachers/id - GET
@teachers_bp.route("/<int:teacher_id>")
def get_teacher(teacher_id):
    teacher = db.session.scalar(db.select(Teacher).filter_by(id=teacher_id))
    if teacher:
        return teacher_schema.dump(teacher)
    else:
        return {"message": f"Teacher with id {teacher_id} does not exist"}, 404

# # Create - /teachers - POST
# @teachers_bp.route("/", methods=["POST"]) 
# def create_teacher():
#     body_data = request.get_json()
#     new_teacher = Teacher(
#         name=body_data.get("name")

#     )