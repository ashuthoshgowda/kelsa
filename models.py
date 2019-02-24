import db


class User(Base):
   __tablename__ = “users”

   id = Column(Integer, primary_key=True)
   name = Column(String)

   def __init__(self, name):
       “”"“”"
       self.name = name

   def __repr__(self):
       return “<Artist: {}>“.format(self.name)


class Tasks(Base):
   “”"“”"
   __tablename__ = “tasks”

   id = Column(Integer, primary_key=True)
   user = Column(String)
   task = Column(String)
   time = Column(String)
   user_id = Column(Integer, ForeignKey(“users.id”))
   artist = relationship(“User”, backref=backref(
       “tasks”, order_by=id))

   def __init__(self, title, release_date, publisher, media_type):
       “”"“”"
       self.user = user
       self.task = task
       self.time = time
