import asyncio
import websockets
import json
from datetime import datetime

class FerroServer:
    def __init__(self):
        self.clients = set()
        self.message_history = []

    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"New connection. Total clients: {len(self.clients)}")

    async def unregister(self, websocket):
        self.clients.remove(websocket)
        print(f"Connection closed. Total clients: {len(self.clients)}")

    async def broadcast(self, message):
        if self.clients:
            message_json = json.dumps({
                "type": "message",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.gather(
                *[client.send(message_json) for client in self.clients]
            )

    async def handler(self, websocket):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.broadcast(message)
                self.message_history.append(message)
        finally:
            await self.unregister(websocket)

async def main():
    server = FerroServer()
    async with websockets.serve(server.handler, "localhost", 8765):
        print("FerroChat server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())