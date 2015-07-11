from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists


engine = create_engine('sqlite:///db/webpy.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# Imports all models and generates metadata
def init_db():
    import webpy.models
    Base.metadata.create_all(bind=engine)

    # Insert plans -- Hardcoded
    # TODO: Remove this and have it dynamically generated

    plan0 = webpy.models.Plan("Anonymous", 10, 100, 0)
    plan1 = webpy.models.Plan("Normal", 10, 500, 3)
    plan2 = webpy.models.Plan("Advanced", 15, 2000, 15)

    plans = [plan0, plan1, plan2]

    for plan in plans:
        # Check if plan exists already
        stmt = exists().where(webpy.models.Plan.name == plan.name and webpy.models.Plane.price == plan.price)
        if db_session.query(stmt).one()[0]:  # if it exists, continue
            continue
        db_session.add(plan)  # Otherwise add it
    db_session.commit()
