# Tic-Tac-Toe

REST API for a tic-tac-toe game

## How to setup and start the game

First clone the repository and change to the project directory

```sh
git clone https://github.com/sanders41/tic-tac-toe.git
cd tic-tac-toe
```

Note: This project uses Poetry to manage dependencies. If you do not already have Poetry installed
you will need to install it with the instuctions [here](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

Next install the dependencies

```sh
poetry install
```

Then start the server

```sh
poetry run uvicorn tic_tac_toe.main:app
```

## How to play

Once the server is running the game API can be accessed at http://localhost:8000/docs

To start a new game click `Try it out` on the `api/v1/game/create` route and click `Execute`. This
will start a new game, and the response will contain the game `id`.

To play the game click `Try it out` on the `api/v1/game/move` route. In the `Request body` section
enter the id you received when creating a new game into the `gameId` field. Then enter your desired
move location in the the `row` and `col` fields. Valid `row` values are between 0 and 2, where 0
is the first row, 1 is the second row, and 2 is the third row. Valid `col` values are between 0 and
2 where 0 is the first column, 1 is the second column, and 2 is the third column.

Once you enter you values click the `Execute` button. In the game you are X and the computer is
O. After clicking `Execute` the server will return the current board state with both your and the
computer's move. Continue in this manner using the same `gameId` until either a winner is reported
in the `winner` field, or a draw is reported.

At any point you can start a new game by accessing the `api/v1/game/create` route again. If you did
not complete a game and want to come back to it you can continue by using the appropriate game id on the
`api/v1/game/move` route.

You can view all completed and in progress games by clicking `Try it out` on the `api/v1/game/all`
route and the clicking `Execute`. You can view the state of an individual game by clicking
`Try it out` on the `api/v1/game/{id}` get route, entering the game's id into the `id` field, and clicking
`Execute`.

Games can be deleted by clicking `Try it out` on the `api/v1/game/{id}` delete route, entering the game
id into the `id` field, and clicking `Execute`.
