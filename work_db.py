import sqlite3
from datetime import datetime


class PostDB:

    def __init__(self, db_root: str):
        self.db_root = db_root

    def __str__(self):
        return f"Post database connector for {self.db_root} root."

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PostDB, cls).__new__(cls)
        return cls.instance

    # Function for adding a new record to a table
    def input_post(self, title: str, description: str, photo: str = '', origin_link: str = '') -> int:
        base = sqlite3.connect(f'{self.db_root}')
        cur = base.cursor()

        try:
            current_time = datetime.now()
            cur.execute("INSERT INTO posts_post (title, description, cover, modified_date, is_published, origin_link) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (title, description, photo, current_time, 0, origin_link)
                        )
            base.commit()

        except Exception as error:
            print(error.__class__, error.args[0])
            return 1

        finally:
            base.close()
        return 0

    # Function to check if there is a record with the given header
    def check_post_on_exist(self, title: str = '', origin_link: str = '') -> bool:
        base = sqlite3.connect(f'{self.db_root}')
        cur = base.cursor()

        try:

            if len(origin_link) > 0:
                cur.execute("SELECT * FROM posts_post WHERE title=? OR origin_link=?", (title, origin_link,))

            else:
                cur.execute("SELECT * FROM posts_post WHERE title=?", (title,))

            result = cur.fetchone()

        except Exception as error:
            print(error.__class__, error.args[0])
            return False

        finally:
            base.close()

        return result is not None

    # Function to get a list of all records where is_published = True and publication_date > datetime.now()
    @property
    def get_upcoming_post(self) -> [tuple]:
        base = sqlite3.connect(f'{self.db_root}')
        cur = base.cursor()

        try:

            cur.execute(
                "SELECT * FROM posts_post WHERE is_published=0 AND publication_date IS NOT NULL ORDER BY "
                "publication_date",
                )
            result = cur.fetchall()

        except Exception as error:
            print(error.__class__, error.args[0])
            return []

        finally:
            base.close()

        return result

    def publish_post(self, post_id: int) -> int:
        base = sqlite3.connect(f'{self.db_root}')
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
