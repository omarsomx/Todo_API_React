from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=False, nullable=False)
    is_done = db.Column(db.Boolean(), unique=False, nullable=False, default=False)

    def __repr__(self):
        return '<Todo %r>' % self.task

    def serialize(self):
        return {
            "id": self.id,
            "email": self.task,
            "is_done": self.is_done,
        }
    
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def create_task(cls, title):
        todo = cls()
        todo.task = title

        db.session.add(todo)
        db.session.commit()

        return todo
    
    def update_task(self, task=None):
        self.task = task if task is not None else self.task

        db.session.commit()

        return True
    
    def destroy(self):
        db.session.delete(self)
        db.session.commit()

        return True