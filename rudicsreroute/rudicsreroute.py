import asyncio

# This module can be used to redirect TCP traffic arriving on one port
# to an other. The intended use is to divert the incoming connection
# from a rudics server to a dockserver to a different dockserver.
#
# There are two classes implemented. One for python 3.7+ and one for python3.6
#
# Use at your own peril.
#
# lucas.merckelbach@hereon.de 8 Mar 2022


# Python version 3.7+
class RerouteServer(object):

    def __init__(self, port, remote_host, remote_port):
        self.port = port
        self.remote_host = remote_host
        self.remote_port = remote_port


    async def forward_transport(self, reader, writer):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            writer.write(data)
            await writer.drain()
            
    async def handle_connection(self, reader, writer):
        reader_remote, writer_remote = await asyncio.open_connection(self.remote_host,
                                                                     self.remote_port)
        tasks = []
        tasks.append(asyncio.create_task(self.forward_transport(reader, writer_remote)))
        tasks.append(asyncio.create_task(self.forward_transport(reader_remote, writer)))

        await asyncio.gather(tasks[0])
        writer.close()
        writer_remote.close()
        
    async def main(self):
        server = await asyncio.start_server(
            self.handle_connection, '127.0.0.1', self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    def run(self):
        asyncio.run(self.main())


# python version 3.6

class RerouteServer36(object):

    def __init__(self, port, remote_host, remote_port):
        self.port = port
        self.remote_host = remote_host
        self.remote_port = remote_port


    async def forward_transport(self, reader, writer):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            writer.write(data)
            await writer.drain()
                    
    async def handle_connection(self, reader, writer):
        reader_remote, writer_remote = await asyncio.open_connection(self.remote_host,
                                                                     self.remote_port)

        task0 = asyncio.ensure_future(self.forward_transport(reader, writer_remote))
        task1 = asyncio.ensure_future(self.forward_transport(reader_remote, writer))
        await asyncio.gather(task0) # wait until the incomming connection drops
        task1.cancel() # cancel the task1
        writer.close()
        writer_remote.close()
        
    async def main(self):
        server = await asyncio.start_server(
            self.handle_connection, '127.0.0.1', self.port)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        #Never stop...
        while True:
            await asyncio.sleep(1)

    def run(self):
        asyncio.run(self.main())


def main():
    import argparse, sys
    description = '''
A simple bi-directional portforwarding program.
'''
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('local_port', type=int,
                        help='port for incomming traffic')
    parser.add_argument('remote_host', type=str,
                        help='remote host')
    parser.add_argument('remote_port', type=int,
                        help='remote port')
    
    args = parser.parse_args()
    if not sys.version_info.major==3 or sys.version_info.minor<=5:
        sys.stderr.write("Only python 3.6+ is supported.\n\n")
        sys.exit(1)
    if sys.version_info.minor==6:
        reroute = RerouteServer36(args.local_port,
                                  args.remote_host,
                                  args.remote_port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(reroute.main()) # never finshes.
    else:
        reroute = RerouteServer(args.local_port,
                                args.remote_host,
                                args.remote_port)
        reroute.run()


