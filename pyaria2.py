#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import xmlrpc.client
import os
import time

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6800
SERVER_URI_FORMAT = 'http://{}:{:d}/rpc'


class PyAria2(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, session=None):

        if not isAria2Installed():
            raise Exception('aria2 is not installed, please install it before.')

        if not isAria2rpcRunning():
            cmd = 'aria2c' \
                  ' --enable-rpc' \
                  ' --rpc-listen-port %d' \
                  ' --continue' \
                  ' --max-concurrent-downloads=20' \
                  ' --max-connection-per-server=10' \
                  ' --rpc-max-request-size=1024M' % port

            if not session is None:
                cmd += ' --input-file=%s' \
                       ' --save-session-interval=60' \
                       ' --save-session=%s' % (session, session)

            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            count = 0
            while True:
                if isAria2rpcRunning():
                    break
                else:
                    count += 1
                    time.sleep(3)
                if count == 5:
                    raise Exception('aria2 RPC server started failure.')
            print('aria2 RPC server is started.')
        else:
            print('aria2 RPC server is already running.')

        server_uri = SERVER_URI_FORMAT.format(host, port)
        self.server = xmlrpc.client.ServerProxy(server_uri, allow_none=True)

    def addUri(self, uris, options=None, position=None):
        return self.server.aria2.addUri(uris, options, position)

    def addTorrent(self, torrent, uris=None, options=None, position=None):
        return self.server.aria2.addTorrent(xmlrpc.client.Binary(open(torrent, 'rb').read()), uris, options, position)

    def addMetalink(self, metalink, options=None, position=None):
        return self.server.aria2.addMetalink(xmlrpc.client.Binary(open(metalink, 'rb').read()), options, position)

    def remove(self, gid):
        return self.server.aria2.remove(gid)

    def forceRemove(self, gid):
        return self.server.aria2.forceRemove(gid)

    def pause(self, gid):
        return self.server.aria2.pause(gid)

    def pauseAll(self):
        return self.server.aria2.pauseAll()

    def forcePause(self, gid):
        return self.server.aria2.forcePause(gid)

    def forcePauseAll(self):
        return self.server.aria2.forcePauseAll()

    def unpause(self, gid):
        return self.server.aria2.unpause(gid)

    def unpauseAll(self):
        return self.server.aria2.unpauseAll()

    def tellStatus(self, gid, keys=None):
        return self.server.aria2.tellStatus(gid, keys)

    def getUris(self, gid):
        return self.server.aria2.getUris(gid)

    def getFiles(self, gid):
        return self.server.aria2.getFiles(gid)

    def getPeers(self, gid):
        return self.server.aria2.getPeers(gid)

    def getServers(self, gid):
        return self.server.aria2.getServers(gid)

    def tellActive(self, keys=None):
        return self.server.aria2.tellActive(keys)

    def tellWaiting(self, offset, num, keys=None):
        return self.server.aria2.tellWaiting(offset, num, keys)

    def tellStopped(self, offset, num, keys=None):
        return self.server.aria2.tellStopped(offset, num, keys)

    def changePosition(self, gid, pos, how):
        return self.server.aria2.changePosition(gid, pos, how)

    def changeUri(self, gid, fileIndex, delUris, addUris, position=None):
        return self.server.aria2.changeUri(gid, fileIndex, delUris, addUris, position)

    def getOption(self, gid):
        return self.server.aria2.getOption(gid)

    def changeOption(self, gid, options):
        return self.server.aria2.changeOption(gid, options)

    def getGlobalOption(self):
        return self.server.aria2.getGlobalOption()

    def changeGlobalOption(self, options):
        return self.server.aria2.changeGlobalOption(options)

    def getGlobalStat(self):
        return self.server.aria2.getGlobalStat()

    def purgeDownloadResult(self):
        return self.server.aria2.purgeDownloadResult()

    def removeDownloadResult(self, gid):
        return self.server.aria2.removeDownloadResult(gid)

    def getVersion(self):
        return self.server.aria2.getVersion()

    def getSessionInfo(self):
        return self.server.aria2.getSessionInfo()

    def shutdown(self):
        return self.server.aria2.shutdown()

    def forceShutdown(self):
        return self.server.aria2.forceShutdown()

    def multicall(self, methods):
        return self.server.aria2.multicall(methods)


def isAria2Installed():
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and 'aria2c' in os.listdir(cmdpath):
            return True

    return False


def isAria2rpcRunning():
    pgrep_process = subprocess.Popen('pgrep -l aria2', shell=True, stdout=subprocess.PIPE)

    if pgrep_process.stdout.readline() == b'':
        return False
    else:
        return True
