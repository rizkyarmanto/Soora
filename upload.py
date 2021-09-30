import ftplib
session = ftplib.FTP('192.168.0.28','webserver','1234')
file = open('waw.wav','rb')
session.storbinary('STOR waw.wav',file)
file.close()
session.quit()