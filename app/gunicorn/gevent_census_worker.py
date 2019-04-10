from gunicorn.workers import ggevent
import gevent
import sys


class GEventOpenCensusWorker(ggevent.GeventWorker):
    def patch(self):
        from gevent import monkey
        monkey.noisy = False

        # if the new version is used make sure to patch subprocess
        if gevent.version_info[0] == 0:
            monkey.patch_all()
        else:
            monkey.patch_all(subprocess=True, thread=False)

        # monkey patch sendfile to make it none blocking
        ggevent.patch_sendfile()

        # patch sockets
        sockets = []
        for s in self.sockets:
            if sys.version_info[0] == 3:
                sockets.append(ggevent.socket(s.FAMILY, ggevent._socket.SOCK_STREAM, fileno=s.sock.fileno()))
            else:
                sockets.append(ggevent.socket(s.FAMILY, ggevent._socket.SOCK_STREAM, _sock=s))
        self.sockets = sockets

