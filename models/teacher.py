from init import db, ma

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False, default="English") # may produce error
    address = db.Column(db.String(100))

class TeacherSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "department", "address")

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)