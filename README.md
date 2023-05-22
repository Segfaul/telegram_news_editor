# `TG News Editor`

Telegram web application for publishing the posts prepared in advance by the parser with a convenient display of the list of posts. The application also provides the ability to CRUD operations to authorized users and select the date of publication of the post.

___

## *Project Status*

***Completed &#10003;***
___
## Functionality
- Basic CRUD operations on posts via Django generic view classes
- NewsParser class, responsible for parsing / shortening / translating news
- The PostDB class for working with the sqlite3 database and implementing the "Singleton" design pattern
- Pyrogram.Client class, responsible for sending messages to chat / group to "pending
- TelegramBot class, responsible for sending links to the web application and fault notifications

## Technologies and Frameworks
- Python 3.11 
- Django 4.2.1
- Pyrogram 2.0.1
- HTML, CSS, JS
- SQLite 3
___

## Installation

1. Clone the repository to the local machine

    ```shell
    git clone https://github.com/Segfaul/telegram_news_editor.git
    ```

2. Go to the repository directory

    ```shell
    cd telegram_news_editor
    ```

3. Create and activate a virtual environment

    ```shell
    python -m venv env
    source env/bin/activate
    ```

4. Set project dependencies

    ```shell
    pip install -r requirements.txt
    ```

5. Configure the configuration file cfg.json (the parser is customized for https://cointelegraph.com)

    ```shell
    nano cfg.json
    ```

6. Go to the news_editor directory

    ```
    cd news_editor
    ```

7. Create database migrations and apply them

    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Create a Django project superuser (admin)

    ```python
    python manage.py createsuperuser
    ```

9. Run the project on localhost in the background

    ```python
    python manage.py runserver &
    ```

10. Navigate to the top level directory

    ```shell
    cd ..
    ```

11. Run the main news parser also in the background

    ```python
    python init.py &
    ```

12. In case of a problem, the program will stop automatically or you can stop execution using

    ```shell
    ps aux | grep ".py"
    kill PID
    ```

13. Go to the site and enter the previously created data of the superuser (step 8)

    ```shell
    http://127.0.0.1:8000
    ```

14. In the future you can deploy the project on a remote server

    ```python
    python manage.py runserver 123.123.123.123:8000 &
    ```
___

## Additional Information

During the development process I noticed some errors in **Telethon** module (*Telethon==1.24.0*), so it was replaced by a more stable **Pyrogram** (*Pyrogram==2.0.106*).

Sending messages to the group was implemented through a user session, since the standard API for telegram bots does not allow to send messages to pending and edit in the menu of the telegram application. Which is quite sad...
___

