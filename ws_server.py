import asyncio
import aiohttp
import websockets


async def handle_client(websocket):

    print()
    print("==============================")
    print("Client connected")
    print("==============================")

    try:

        async for message in websocket:

            print()
            print("========== WEBSOCKET ==========")
            print("Message received:", message)

            try:

                timeout = aiohttp.ClientTimeout(
                    total=None
                )

                async with aiohttp.ClientSession(
                    timeout=timeout
                ) as session:

                    async with session.post(
                        "http://127.0.0.1:5000/chat",
                        json={
                            "message": message
                        }
                    ) as response:

                        print(
                            "Flask status:",
                            response.status
                        )

                        print(
                            "Content-Type:",
                            response.headers.get(
                                "Content-Type"
                            )
                        )

                        print(
                            "Transfer-Encoding:",
                            response.headers.get(
                                "Transfer-Encoding"
                            )
                        )

                        print()
                        print(
                            "========== STREAM START =========="
                        )

                        async for chunk in response.content.iter_any():

                            if not chunk:
                                continue

                            text = chunk.decode(
                                "utf-8",
                                errors="ignore"
                            )

                            print(
                                "WS CHUNK:",
                                repr(text)
                            )

                            await websocket.send(text)

                        print()
                        print(
                            "========== STREAM END =========="
                        )

            except Exception as error:

                print()
                print(
                    "WEBSOCKET ERROR:",
                    type(error).__name__
                )

                print(
                    "ERROR:",
                    str(error)
                )

                await websocket.send(
                    "\nSorry, I couldn't process your request."
                )

    except websockets.exceptions.ConnectionClosed:

        print("Client disconnected")


async def main():

    print()
    print("==============================")
    print("WebSocket server started")
    print("Listening on ws://localhost:8765")
    print("==============================")

    async with websockets.serve(
        handle_client,
        "localhost",
        8765
    ):

        await asyncio.Future()


asyncio.run(main())