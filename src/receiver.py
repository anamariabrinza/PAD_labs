#!/usr/bin/env python3
import asyncio
import json

@asyncio.coroutine
def get_message(loop):
    reader, writer = yield from asyncio.open_connection(
        '127.0.0.1', 14141, loop=loop
    )

    writer.write(json.dumps({
        'type': 'command',
        'command': 'read'
    }).encode('utf-8'))
    f = open("messages/received.txt", "a+")

    writer.write_eof()
    yield from writer.drain()


    response = yield from reader.read()

    f.write(str(response) + "\n")
    writer.close()
    f.close()

    f2 = open("messages/data.txt", "w")
    f2.write(" ")
    f2.close()

    return response


@asyncio.coroutine
def run_receiver(loop):
    i = 0
    while True:
        i = i + 1
        try:

            response = yield from get_message(loop)
            print("{0}: {1}".format(i,response ))
            yield from asyncio.sleep(1)


        except KeyboardInterrupt:
            #compararea

            break




def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_receiver(loop))



if __name__ == '__main__':
    main()
