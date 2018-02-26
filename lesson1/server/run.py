# -*- coding: utf-8 -*-
import socket
import os

def answ(msg, status = "200 OK", cont_type = "text", ):
    return "HTTP/1.1 " + status + "\r\n" + "Server: simplehttp\r\n" + "Connection: close\r\n" + "Content-Type: " + cont_type +\
        "\r\n" + "Content-Length: " + bytes(len(msg)) + "\r\n" + "\r\n" + msg

def get_response(request):
    headers = request.split('\r')
    header_1 = headers[0].split(' ')
    url = header_1[1]
    adress = url.split('/')
    adress.append('')
    if adress[1] == '':
        for line in headers:
            if line.find('User-Agent') != -1:
                msg = """<!DOCTYPE html>"""\
                      + """<html><head><title>localhost</title></head><body><h1>""" +\
                      """<br>Hello, mister </br>""" \
                      + """<br>You are: """ + line + """</br></h1></body></html>"""
                return answ(msg)
    if adress[1] == 'test':
        msg = """<!DOCTYPE html>"""\
              + """<html><head><title>localhost</title></head><body><h1>""" +\
              """<br>""" + request + """</br></h1></body></html>"""
        return answ(msg)
    if adress[1] == 'media':
        if adress[2] == '':
            files = os.listdir('../files')
            msg = """<!DOCTYPE html>""" \
                  + """<html><head><title>localhost</title></head><body><h1>""" + \
                  """<br><a href="../media/test1.txt">""" + files[0] + """</a></br>""" + \
                  """<br><a href="../media/test2.txt">""" + files[1] + """</a></br>""" + \
                  """</h1></body></html>"""
            return answ(msg)
        try:
            file = open('../files/' + adress[2])
        except:
            msg = """<!DOCTYPE html>""" \
                  + """<html><head><title>localhost</title></head><body><h1>""" + \
                  """<br>""" + "File not found" + """</br></h1></body></html>"""
            return answ(msg, status="404 Not Found")
        msg = """<!DOCTYPE html>""" \
                  + """<html><head><title>localhost</title></head><body><h1>""" + \
                  """<br>""" + file.read() + """</br>""" + \
                  """</h1></body></html>"""
        return answ(msg)
    msg = """<!DOCTYPE html>""" \
          + """<html><head><title>localhost</title></head><body><h1>""" + \
          """<br>""" + "Page not found" + """</br></h1></body></html>"""
    return answ(msg, status="404 Not Found")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # host, server port
server_socket.listen(0)  # listening fo socket server_socket, the allowed amount of queue is 0

print "Started"

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # printing clients IP in console
        request_string = client_socket.recv(2048)  # getting client data from socket client_socket
        client_socket.send(get_response(request_string))  # sending data in socket client_socket
        client_socket.close()
    except KeyboardInterrupt:  # server stop
        print 'Stopped'
        server_socket.close()  # close of the socket server_socket
        exit()