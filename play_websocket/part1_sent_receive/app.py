# -*- coding:utf-8 -*-

import asyncio
import itertools
import json

import websockets

from connect4 import Connect4, PLAYER1, PLAYER2

# https://websockets.readthedocs.io/en/stable/intro/tutorial1.html

# old_1
# async def handler(websocket):
#     while True:
#         message = await websocket.recv()
#         print(message)

# old_2
# async def handler(websocket):
#     while True:
#         try:
#             message = await websocket.recv()
#         except websockets.ConnectionClosedOK:
#             print(f"客户端连接已断开...")
#             break
#         print(message)

# async def handler(websocket):
#     # 客户端每次连接，都会执行handler
#     # This pattern(即上面的old_2) is so common that websockets provides a shortcut
#     # for iterating over messages received on the connection until the client disconnects:
#     async for message in websocket:
#         print(message)


# async def handler(websocket):
#     for player, column, row in [
#         (PLAYER1, 3, 0),
#         (PLAYER2, 3, 1),
#         (PLAYER1, 4, 0),
#         (PLAYER2, 4, 1),
#         (PLAYER1, 2, 0),
#         (PLAYER2, 1, 0),
#         (PLAYER1, 5, 0),
#     ]:
#         event = {
#             "type": "play",
#             "player": player,
#             "column": column,
#             "row": row,
#         }
#         await websocket.send(json.dumps(event))
#         await asyncio.sleep(0.5)
#     event = {
#         "type": "win",
#         "player": PLAYER1,
#     }
#     await websocket.send(json.dumps(event))


async def handler(websocket):
    # Initialize a Connect Four game.
    game = Connect4()

    # Players take alternate turns, using the same browser.
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        try:
            # Play the move.
            row = game.play(player, column)
        except RuntimeError as exc:
            # Send an "error" event if the move was illegal.
            event = {
                "type": "error",
                "message": str(exc),
            }
            await websocket.send(json.dumps(event))
            continue

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))

        # If move is winning, send a "win" event.
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            await websocket.send(json.dumps(event))

        # Alternate turns.
        player = next(turns)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
