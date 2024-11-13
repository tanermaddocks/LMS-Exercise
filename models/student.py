from init import db, ma

class Student(db.Model):
    # table name and primary key
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    # other columns
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(100))

class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "address")

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)