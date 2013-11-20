
import redis
import gevent


class EventBackend(object):
    """
    Interface for registering events and updating clients.
    """

    def __init__(self, redis_url, redis_channel):
        self.clients = list()
        self.redis = redis.from_url(redis_url)
        self.redis_channel = redis_channel
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(redis_channel)

    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            yield data

    def publish(self, event):
        """
        Publish an event to listening clients
        """
        self.redis.publish(self.redis_channel, event)

    def register(self, client):
        """
        Register a WebSocket connection for Redis updates.
        """
        self.clients.append(client)

    def send(self, client, data):
        """
        Send given data to the registered client.
        Automatically discards invalid connections.
        """
        try:
            client.send(data)
        except Exception:
            self.clients.remove(client)

    def run(self):
        """
        Listens for new messages in Redis,
        and sends them to clients.
        """
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """
        Maintains Redis subscription in the background.
        """
        gevent.spawn(self.run)