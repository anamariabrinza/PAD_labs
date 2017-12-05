#!/usr/bin/env python3
import asyncio
import json

from django.contrib.gis import feeds


@asyncio.coroutine
def send_message(message, loop):
    i = 0

    reader, writer = yield from asyncio.open_connection(
        '127.0.0.1', 14141, loop=loop
    )
    payload = json.dumps({
        'type': 'command',
        'command': 'send',
        'payload': message
    }).encode('utf-8')

    writer.write(payload)
    writer.write_eof()
    yield from writer.drain()
    #print (message)


    f = open("messages/data.txt".format(i), "a+")  # create new file
    # name = id_data (timestamp)

    f.write(message + "\n")
    f.close()


    response = yield from reader.read(2048)
    writer.close()



    return response


MESSAGE = 'Hello, Ana'

@asyncio.coroutine
def run_sender(loop):
    i = 0
    while True:
        i = i+1
        try:

            message = '{0}: Just sending a Mess:  {1}'.format(i, MESSAGE)
            #print('Sending %s' % (message,))
            response = yield from send_message(message, loop)
            #print('Received %s', response)
            yield from asyncio.sleep(1)
        except KeyboardInterrupt:
            break


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_sender(loop))


if __name__ == '__main__':
    main()
