from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declaritive import declaritive_base

engine = create_engine('sqlite://db/webpy.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                         bind=engine))

Base = declaritive_base()
Base.query = db_session.query_property()


def init_db():
    import models
    models.users.User
    models.plan
    Base.metadata.create_all(bind=engine)
