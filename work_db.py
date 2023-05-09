import sqlite3
from datetime import datetime


# Function for adding a new record to a table
def input_post(db_name: str, title: str, description: str, photo: str = '') -> int:
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()

    try:
        current_time = datetime.now()
        cur.execute("INSERT INTO posts_post (title, description, cover, modified_date, is_published) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (title, description, photo, current_time, 0)
                    )
        base.commit()

    except Exception as error:
        print(error.__class__, error.args[0])
        return 1

    finally:
        base.close()
    return 0


# Function to check if there is a record with the given header
def check_post_on_exist(db_name: str, title: str) -> bool:
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()

    try:

        cur.execute("SELECT * FROM posts_post WHERE title=?", (title,))
        result = cur.fetchone()

    except Exception as error:
        print(error.__class__, error.args[0])
        return False

    finally:
        base.close()

    return result is not None


# Function to get a list of all records where is_published = True and publication_date > datetime.now()
def get_upcoming_post(db_name: str) -> [tuple]:
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()

    try:

        cur.execute(
            "SELECT * FROM posts_post WHERE is_published=0 AND publication_date IS NOT NULL ORDER BY publication_date",
            )
        result = cur.fetchall()

    except Exception as error:
        print(error.__class__, error.args[0])
        return []

    finally:
        base.close()

    return result


def publish_post(db_name: str, post_id: int) -> int:
    base = sqlite3.connect(f'{db_name}')
    cur = base.cursor()

    try:

        cur.execute('UPDATE posts_post SET is_published = ? WHERE id = ?', (True, post_id))
        base.commit()

    except Exception as error:
        print(error.__class__, error.args[0])
        return 1

    finally:
        base.close()

    return 0
