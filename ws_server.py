
import asyncio
import aiohttp
import websockets


FLASK_URL = "http://127.0.0.1:5000/chat"
END_MARKER = "[[STREAM_END]]"


async def handle_client(websocket):

    print()
    print("==============================")
    print("Client connected")
    print("==============================")

    timeout = aiohttp.ClientTimeout(total=None)

    # Keep the same Flask session across messages
    async with aiohttp.ClientSession(
        timeout=timeout,
        cookie_jar=aiohttp.CookieJar(unsafe=True)
    ) as session:

        try:

            async for message in websocket:

                print()
                print("========== WEBSOCKET ==========")
                print("Message received:", message)

                try:

                    async with session.post(
                        FLASK_URL,
                        json={
                            "message": message
                        }
                    ) as response:

                        print(
                            "Flask status:",
                            response.status
                        )

                        content_type = response.headers.get(
                            "Content-Type",
                            ""
                        )

                        print(
                            "Content-Type:",
                            content_type
                        )

                        print(
                            "Transfer-Encoding:",
                            response.headers.get(
                                "Transfer-Encoding"
                            )
                        )

                        print()
                        print("========== STREAM START ==========")

                        # Handle Flask JSON responses
                        if "application/json" in content_type:

                            result = await response.json(
                                content_type=None
                            )

                            reply = result.get(
                                "reply",
                                "No response received from Flask."
                            )

                            print(
                                "WS REPLY:",
                                repr(reply)
                            )

                            await websocket.send(str(reply))

                        # Forward plain-text streaming responses
                        else:

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

                        # Signal completion to the frontend
                        await websocket.send(END_MARKER)

                        print()
                        print("========== STREAM END ==========")

                except Exception as error:

                    print()
                    print(
                        "WEBSOCKET ERROR:",
                        type(error).__name__
                    )

                    print("ERROR:", str(error))

                    try:
                        await websocket.send(
                            "Sorry, I couldn't process your request."
                        )

                        await websocket.send(END_MARKER)

                    except websockets.exceptions.ConnectionClosed:
                        break

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


if __name__ == "__main__":
    asyncio.run(main())
