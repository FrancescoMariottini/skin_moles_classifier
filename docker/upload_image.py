from PIL import Image, ImageFile
from gevent.queue import Empty, Queue
from gevent.event import AsyncResult
from gevent.timeout import Timeout
import time
MAX_IMAGES = 10
MAX_DURATION = 300
DATA_DIR = 'data'
MAX_IMAGE_SIZE = 800, 600
BROADCAST_QUEUE = Queue()
KEEP_ALIVE_DELAY = 25


def broadcast(message):
    """Notify all waiting waiting gthreads of message."""
    waiting = []
    try:
        while True:
            waiting.append(BROADCAST_QUEUE.get(block=False))
    except Empty:
        pass
    print('Broadcasting {} messages'.format(len(waiting)))
    for item in waiting:
        item.set(message)


def safe_addr(ip_addr):
    """Strip off the trailing two octets of the IP address."""
    return '.'.join(ip_addr.split('.')[:2] + ['xxx', 'xxx'])


def save_normalized_image(path, data):
    """Generate an RGB thumbnail of the provided image."""
    image_parser = ImageFile.Parser()
    try:
        image_parser.feed(data)
        image = image_parser.close()
    except IOError:
        return False
    image.thumbnail(MAX_IMAGE_SIZE, Image.ANTIALIAS)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(path)
    return True


def receive():
    """Generator that yields a message at least every KEEP_ALIVE_DELAY seconds.
    yields messages sent by `broadcast`.
    """
    now = time.time()
    end = now + MAX_DURATION
    tmp = None
    # Heroku doesn't notify when clients disconnect so we have to impose a
    # maximum connection duration.
    while now < end:
        if not tmp:
            tmp = AsyncResult()
            BROADCAST_QUEUE.put(tmp)
        try:
            yield tmp.get(timeout=KEEP_ALIVE_DELAY)
            tmp = None
        except Timeout:
            yield ''
        now = time.time()


def event_stream(client):
    """Yield messages as they come in."""
    force_disconnect = False
    try:
        for message in receive():
            yield 'data: {}\n\n'.format(message)
        print('{} force closing stream'.format(client))
        force_disconnect = True
    finally:
        if not force_disconnect:
            print('{} disconnected from stream'.format(client))
