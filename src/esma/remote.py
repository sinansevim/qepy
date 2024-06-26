import paramiko
from dotenv import dotenv_values

config = dotenv_values(".env")
hostname=config['hostname']
username=config['username']
password=config['password']

def exec(command):
    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        # Establish SSH connection
        client.connect(hostname, username=username)

        # Submit our Grid Engine job by running a remote 'qsub' command over SSH
        stdin, stdout, stderr = client.exec_command(command)

        # Show the standard output and error of our job
        print("Standard output:")
        out = stdout.read()
        lines = out.decode('utf-8').split("\n")
        for line in lines:
            print(line)

def put(payload,destination):
    try:
        hostname=config['sftp']
    except:
        pass
    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        # client.set_missing_host_key_policy(paramiko.WarningPolicy)

        # Establish SSH connection
        client.connect(hostname, username=username,password=password)


        # # Establish SFTP connection
        with client.open_sftp() as sftp:
        #     # Push job submission script to a particular path on the cluster
            sftp.put(payload, destination)


def get(payload,destination):
    try:
        hostname=config['sftp']
    except:
        pass
    with paramiko.SSHClient() as client:
        client.load_system_host_keys()
        # client.set_missing_host_key_policy(paramiko.WarningPolicy)

        # Establish SSH connection
        client.connect(hostname, username=username,password=password)


        # # Establish SFTP connection
        with client.open_sftp() as sftp:
        #     # Push job submission script to a particular path on the cluster
            sftp.get(payload, destination)

