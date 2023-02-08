from typing import Set
from collections import namedtuple
from fastapi import WebSocket, WebSocketDisconnect
from app.utils.logger import logger


class ConnectionManager:
    def __init__(self):
        self.device = namedtuple('OnlineDevice', 'client_id websocket')
        self.active_connections: Set[self.device] = set()

    async def connect(self, websocket: WebSocket, client_id: int):
        """链接"""
        await websocket.accept()
        new_device = self.device(client_id=client_id, websocket=websocket)
        if new_device not in self.active_connections:
            self.active_connections.add(new_device)
        logger.bind(websocket=True).info("Client connect {}".format(client_id))

    def __len__(self):
        """当前用户数"""
        return len(self.active_connections)

    def disconnect(self, websocket: WebSocket, client_id: int):
        """断开链接"""
        self.active_connections.discard(self.device(
            client_id=client_id, websocket=websocket))

    async def send_personal_message(self, message: str, client_id: int):
        """发送消息"""
        for connection in self.active_connections:
            if connection.client_id == client_id:
                logger.bind(websocket=True).info("Send to {}: {}".format(client_id, message))
                try:
                    await connection.websocket.send_text(message)
                except WebSocketDisconnect:
                    self.disconnect(connection.websocket, connection.client_id)

    async def broadcast(self, message: str):
        """广播"""
        for connection in self.active_connections:
            try:
                logger.bind(websocket=True).info("Broadcast: {}-{}".format(connection.client_id, message))
                await connection.websocket.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection.websocket, connection.client_id)


manager = ConnectionManager()
