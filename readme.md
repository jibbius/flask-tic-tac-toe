# Flask Tic Tac Toe

## About

The intent for this project is to allow a user to play a game of Tic Tac Toe.

This is my final project for General Assembly's Python Programming course.

As part of this project, I am seeking to test my competencies with Flask and Persisting Data.

## Deployment Steps

### Prerequisites

    mkdir flask-tic-tac-toe
    git clone https://github.com/jibbius/flask-tic-tac-toe.git flask-tic-tac-toe
    cd flask-tic-tac-toe

    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-venv
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

### Execute
    source .venv/bin/activate
    python3 flask_app.py

## Config

- Configuration is stored in `/config/__init__.py`.
- By default, data is persisted to a sqlite database file (`database.db`)
- This behaviour can be modified to connect to your database server of choice, by modifying
  `SQLALCHEMY_DATABASE_URI`  to specify an appropriate connection string.
  - Alternatively, `"sqlite:///:memory:"` can be specified to persist to memory only.
- A secret key, (`SECRET_KEY`), also gets recorded in config.py
  - In a production context, this should be set via environment variables

## Running

- By default, runs on [http://127.0.0.1:5000](http://127.0.0.1:5000)
- Start a new game 

## Features

The application includes the following features:

- Ability to load initial list of Players from CSV file.
- Ability to VIEW/ADD/UPDATE* to list of Players via API.
  - Note:
  - 'DELETE' has intentionally been excluded.
  - It is anticipated that removing users will not be allowed.
  - This is for the purpose of maintaining foreign key integrity.
  - A logical delete (i.e. Player.Deleted = 'Y') might eventually be added; but would utilise the UPDATE method rather than DELETE.
- HTML + JS forms to test the set of Player APIs.
- Ability to synchronise list of Players back to CSV file.
- Ability to create a game of Tic Tac Toe.
- Ability to assign players to a game.
- Ability for HUMAN players to submit moves, to progress a game.
- Ability for COMPUTER players to submit moves, to progress a game.
- Ability for a game to determine its winner.
- Game results to be persisted.
- Persistence layer to be migrated to database, rather than CSV.
- A UI that is (more) usable by humans.

## Planned Features

- Different difficulty levels for computer controlled players
- UI Improvements
- Ability to view historical game statistics (winner; state of game board).
- Database performance tuning.
- 3D tic tac toe

## Acknowledgments
- The Team at General Assembly, and the Python Programming course.
  - Geoff
  - Arnab
  - Lillian
- Mastering Flask Web Development (book by Daniel Gaspar + Jack Stouffer)
- Software Design in Python (YouTube series by  ArjanCodes)
- CodePen.io
- Twitter Bootstrap
