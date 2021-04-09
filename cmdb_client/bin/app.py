from concurrent.futures import ThreadPoolExecutor
from lib.plugins import get_server_info
from settings import settings
import requests
import paramiko

def ssh(hostname,command):
    private_key = paramiko.RSAKey.from_private_key_file(settings.SSH_PRIVATE_KEY_PATH)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=settings.SSH_PORT, username=settings.SSH_USER, pkey=private_key)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read()
    ssh.close()
    return result.decode('utf-8')

def task(hostname):
    info = get_server_info(hostname, ssh)

    requests.post(
        url="http://127.0.0.1:8000/api/v1/server/",
        json={'hostname':hostname,'info':info}
    )

def run():
    response = requests.get(url="http://127.0.0.1:8000/api/v1/server/")
    host_list = response.json()
    pool = ThreadPoolExecutor(settings.THREAD_POOL_SIZE)
    for host in host_list:
        pool.submit(task,host)

if __name__ == '__main__':
    run()