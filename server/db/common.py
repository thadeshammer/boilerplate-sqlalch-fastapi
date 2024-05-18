from sqlalchemy.ext.declarative import declarative_base

# When I tried homing this in __init__.py it got weird, and a lot of examples I saw didn't
# use __init__.py, so maybe that's why? This works.
# It does need to be in a SINGLE PLACE IN THE APP from which everything else grabs it, otherwise
# you'll end up with multiple virtual databases, and - unless you're lucky - the one with the tables
# won't be the one with the literal db connection. DBs are weird and Python makes it tricker than
# normal.

Base = declarative_base()
