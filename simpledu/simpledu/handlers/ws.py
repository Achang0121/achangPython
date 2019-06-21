import redis
import gevent
from flask import Blueprint

ws = Blueprint('ws', __name__, url_prefix='/ws')

# 创建 redis 连接
redis = redis.from_url('redis://127.0.0.1:6379')


class Chatroom(object):
    
    def __init__(self):
        self.clients = []
        # 初始化 pubsub 系统
        self.pubsub = redis.pubsub()
        # 订阅 chat 频道
        self.pubsub.subscribe('chat')
        
    def register(self, client):
        self.clients.append(client)
        
    def send(self, client, data):
        # 给每一个客户端 client 发送消息 data
        try:
            # python3 中接收的消息是二进制的，使用 decode 方法转码
            client.send(data.decode('utf-8'))
        except:
            # 发生错误可能是客户端已经关闭，移除该客户端
            self.clients.remove(client)
            
    def run(self):
        # 依次将接收到的消息再发给所有客户端
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    # 使用 gevent 异步发送 
                    gevent.spawn(self.send, client, data)
                    
    def start(self):
        # 异步执行 run 函数
        gevent.spawn(self.run)
        
        
# 初始化聊天室
chat = Chatroom()
chat.start()

@ws.route('/send')
def inbox(ws):
    # 使用 flask-scokets, ws 链接对象会被自动注入到路由处理函数，该函数处理前端发过来的消息
    # 下面的 while 循环，里面的 receive() 函数实际是在阻塞运行的，直到前端发送消息过来
    # 消息会被放入到 chat 频道，也就所队列消息中，这样一直循环，直到websocket连接关闭
    while not ws.closed:
        message = ws.receive()
        
        if message:
            redis.publish('chat', message)
            
@ws.route('/recv')
def outbox(ws):
    # 该函数用来注册客户端连接，并在 chatroom 中将其他客户端接收的消息发送给这些客户端
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)