import json, asyncio
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.extensions import websocket_manager


router_message_admin = APIRouter()



@router_message_admin.get('/index/', deprecated=True)
async def index():
    """首页"""
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <form action="" onsubmit="sendMessage(event)">
                <label>Channel: <input type="text" id="Channel" autocomplete="off" value="default"/></label>
                <label>Client_id: <input type="text" id="client_id" autocomplete="off" value="yunjing01"/></label>
                <button onclick="connect(event)">Connect</button>
                <hr>
                <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
            var ws = null;
                function connect(event) {
                    var itemId = document.getElementById("Channel")
                    var token = document.getElementById("client_id")
                    ws = new WebSocket("ws://127.0.0.1:8399/message/client" + "/ws?channel=" + itemId.value + "&client_id=" + token.value);
                    ws.onmessage = function(event) {
                        var messages = document.getElementById('messages')
                        var message = document.createElement('li')
                        var content = document.createTextNode(event.data)
                        message.appendChild(content)
                        messages.appendChild(message)
                    };
                    event.preventDefault()
                }
                function sendMessage(event) {
                    var input = document.getElementById("messageText")
                    ws.send(input.value)
                    input.value = ''
                    event.preventDefault()
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html)


@router_message_admin.websocket('/ws')
async def websocket_endpoint(
    websocket: WebSocket,
    channel: str = Query(default=None, description='频道名称'),
    client_id: str = Query(default=None, description='频道客户端ID')
):
    await websocket_manager.add_to_channel(channel, client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.broadcast_to_channel(channel, json.dumps(data))
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        await websocket_manager.leave_to_channel(channel, client_id, websocket)
