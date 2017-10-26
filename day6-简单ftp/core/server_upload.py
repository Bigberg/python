# -*- coding: UTF-8 -*-

from core import FtpServer

if __name__ == '__main__':
    ftp_server = FtpServer.FtpServer('localhost', 8888)
    ftp_server.server_upload()
