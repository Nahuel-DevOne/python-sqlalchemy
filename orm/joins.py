from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

engine = create_engine('postgresql://postgres:@localhost/pythonpg')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())
    courses = relationship('Course', backref='user') # creando la relación
    
    def __str__(self):
        return self.username
    
class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    user_id = Column(ForeignKey('users.id'))  
    created_at = Column(DateTime(), default=datetime.now()) 
    
    def __str__(self):
        return self.title 
        
# un usuario puede tener múltiples cursos y un curso le pertenece a un usuario    
Session = sessionmaker(engine)   
session = Session() 

if __name__ == '__main__':
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    user1 = User(username='user1', email='user1@example.com')
    user2 = User(username='user2', email='user2@example.com')    
    user3 = User(username='user3', email='user3@example.com')    
    user4 = User(username='user4', email='user4@example.com')    
    
    # acceso a relaciones mediante objetos
    # de una manera
    course1 = Course(title='Curso profesional de Base de Datos')
    user1.courses.append(
        course1
    )
    
    # de otra manera, aplicando directamente
    user1.courses.append(
        Course(title='Curso profesional de Python')
    )
    
    user1.courses.append(
        Course(title='Curso profesional de JavaScript')
    )
    
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    
    session.commit()
    
    # 1) Listar en consola todos los usuarios que posean por lo menos un curso (INNER JOIN)
    # 2) Listar en consola todos los usuarios sin cursos (LEFT JOIN).
    
    # 1) Inner Join
    ##### Sin clave foránea, que no es este el caso
    # users = session.query(User).join(
    #     Course, User.id == Course.user_id
    # )
    
    ##### Con clave foránea, que es este el caso
    # users = session.query(User).join(
    #     Course
    # )
    
    # for user in users:
    #     print(user)
    
    # 2) Left Join
    users = session.query(User).outerjoin(
        Course
    ).filter(
        Course.id == None
    )
    
    for user in users:
        print(user)
        
        
    