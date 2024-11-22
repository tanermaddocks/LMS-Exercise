from init import db, ma

class Enrolment(db.Model):
    __tablename__ = "enrolments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    enrolment_date = db.Column(db.String(100))

    student = db.relationship("Student", back_populates="enrolments")
    course = db.relationship("Course", back_populates="enrolments")

class EnrolmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "student_id", "course_id", "enrolment_date")

enrolment_schema = EnrolmentSchema()
enrolments_schema = EnrolmentSchema(many=True)