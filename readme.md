# Toy Example Minimal Boilerplate python fastapi sqlalchemy with rate-limiting

That sounds like chat-gpt named it but it was, in fact, me. This example is simplistic and straightforward by design. It's meant to get you moving. Good luck!

## Quick Start

Pull it down, start docker, run:
```
docker-compose build && docker-compose up
```
Then open up the Swagger UI via `localhost/docs`

There are only two VERY simple endpoints in this example.

* `/test` takes a string 'name' and sticks it into the DB along with a generated UUID.
* `/getnames` will spit out everything in that table.

**NOTE the DB is not persisted outside of its container** so if you destroy/rebuild the container, that data is gone. If you don't want that, you'll need to mount a volume for it.

## What's Inside

### Docker

**DB** This example uses postgres but I also tested it against mysql and sqlite3.
**SERVER** FastAPI on uvicorn, see `requirements.txt` for libraries you'll need. Runs on port 80.

### Python

I'm using 3.11 in this example, but since FastAPI has a dependency on wheel, you might find that your IDE (looking at you VSCode) will always be unhappy with FastAPI; this is because - I've learned - the maintainers of wheel deprioritize Windows. Since the app itself runs dockerized, it will work. You just have to deal with the red squigglies.

* **fastapi** run on uvicorn with hot-reload.
* **slowapi** with a simplistic example of rate-limiting
* **sqlalchemy** ORM with:
 * a test model that creates an associated table in the db if it doesn't exist.
 * bare minimum setup to get python and the db talking
* **pydantic** for the SQLAlchemy to FastAPI communication. (I learned about SQLModel later.)