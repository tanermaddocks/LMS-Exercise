from marshmallow import fields

from init import db, ma

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    duration = db.Column(db.Float, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    teacher = db.relationship("Teacher", back_populates="courses")
    enrolments = db.relationship("Enrolment", back_populates="course", cascade="all, delete")

class CourseSchema(ma.Schema):
    ordered = True
    teacher = fields.Nested("TeacherSchema", only=["name", "department"])
    enrolments = fields.List(fields.Nested("EnrolmentSchema", exclude=["course"]))
    class Meta:
        fields = ("id", "name", "duration", "teacher_id", "teacher", "enrolments")

course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)