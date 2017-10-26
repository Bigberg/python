# -*- coding: UTF-8 -*-

from core.FtpServer import FtpServer

if __name__ == '__main__':
    ftp_server = FtpServer('localhost', 8887)
    ftp_server.server_download()
