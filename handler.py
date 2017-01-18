import os
import subprocess

libdir = os.path.join(os.getcwd(), 'local', 'lib')

def handler(event, context):
    command = 'LD_LIBRARY_PATH={} python worker.py'.format(libdir)
    output = subprocess.check_output(command, shell=True)

    print output

    return 
