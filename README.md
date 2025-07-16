# Superhero API

This is a Django/DRF project that integrates with the external [SuperHero API](https://superheroapi.com/) to store and search for superhero data in database.

## Features

- Import a hero by name from SuperHeroAPI via POST
- Store hero attributes (intelligence, strength, speed and power) (can be `null`)
- Filter/search heroes using flexible numeric lookups
- Case-insensitive exact matching by name

---

## Endpoints

### `POST /hero/`

**Description:**
Searches for a hero by name using the SuperHero API and then saves it in the database (if not already stored).

**Request body:**

```json
{
  "name": "Batman"
}
```

**Behavior:**

- If a hero with this name is found and not in DB, it's saved and returned.
- If not found, returns `404` with an error message.
- If the hero already exists, returns `400` with an error message.

---

### `GET /hero/`

**Description:**
Returns a filtered list of heroes from the local database.

#### Query parameters (all optional):

##### Name (case-insensitive exact match):


| Parameter | Example        | Description                  |
| --------- | -------------- | ---------------------------- |
| `name`    | `?name=batman` | Case-insensitive exact match |

##### Numeric fields (`intelligence`, `strength`, `speed`, `power`):

##### Examples:


| Lookup           | Query Param         | Example              |
| ---------------- | ------------------- | -------------------- |
| exact match      | `<field_name>`      | `?strength=90`       |
| greater than     | `<field_name>__gt`  | `?strength__gt=80`   |
| greater or equal | `<field_name>__gte` | `?strength__gte=80`  |
| less than        | `<field_name>__lt`  | `?strength__lt=100`  |
| less or equal    | `<field_name>__lte` | `?strength__lte=100` |

You can combine multiple filters:

```
/hero/?intelligence__gte=80&power__lte=90
```

---

## Example Use Cases

- Get all heroes with `strength` between 70 and 100:

  ```
  /hero/?strength__gte=70&strength__lte=100
  ```
- Get a hero named "IronMan", regardless of case:

  ```
  /hero/?name=ironman
  ```

---

## Setup and Usage

This project is prefered to run with `Docker compose`.

First you will need to get the code itself:

```bash
git clone https://github.com/ksmvrheee/superheroes.git
cd superheroes

```

Then you'll need to fill the .env file that contains environmental variables crucial for project to work.

### Environmental variables


| Variable                    | Role                                                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| SUPERHEROAPI_TOKEN          | Your access-token for superheroapi                                                                                           |
| DJANGO_SECRET_KEY           | Django secret key                                                                                                            |
| DEBUG                       | Django DEBUG variable (True/False)                                                                                           |
| DJANGO_ALLOWED_HOSTS        | List of allowed hosts for Django deployment (separated by commas)                                                            |
| DJANGO_PORT                 | Port for Django (8000 by default)                                                                                            |
|                             |                                                                                                                              |
| DJANGO_CSRF_TRUSTED_ORIGINS | List of trusted CSRF sources for Django (comma separated, with protocol (‘https://’), can be similar to the previous item) |
| DATABASE_ENGINE             | DB engine (postgresql_psycopg2 for PostgreSQL).                                                                              |
| DATABASE_NAME               | DB name                                                                                                                      |
| DATABASE_USERNAME           | Username for the DB                                                                                                          |
| DATABASE_PASSWORD           | Password for the DB user                                                                                                     |
| DATABASE_HOST               | DB host (`db` by default, you should not modify that)                                                                        |
| DATABASE_PORT               | Port for the DB (`5432` for PostgreSQL by default, you should not modify that)                                               |

After you filled the .env-file you can launch the project:

```bash
docker compose up --build
```

Now configure the ports and firewall and the application is ready to use.

## Testing (optional)

To run project unit-tests (inside a running container) you can enter the container's terminal and execute a command to launch Django testing:

```bash
docker exec -it django-docker bash
python3 manage.py test
```