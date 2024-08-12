## Setup

* Make sure you have MariaDB set up, e.g. with:

    docker run -p 3306:3306 --detach --name comments-mariadb \
        --env MARIADB_USER=comments_admin \
        --env MARIADB_PASSWORD="let it be, let it be" \
        --env MARIADB_DATABASE=comments_db \
        --env MARIADB_ROOT_PASSWORD=my-secret-pw \
        mariadb:latest

* [Install C bindings](https://mariadb.com/docs/server/connect/programming-languages/c/install/) (try `brew install mariadb-connector-c` on MacOS)
* Install all required packages (preferably in a virtualenv) with `pip install -e .`
* Set up the database credentials in `.env` (if you use the docker image you can just use the defaults):

    DB_USERNAME=some_user
    DB_PASSWORD=the-users-password
