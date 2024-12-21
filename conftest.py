import paramiko
import subprocess
import pytest

# Server connection details
SERVER_IP = ''  # Replace with your server's IP
USERNAME = ''  # Replace with your username
PASSWORD = ''  # Replace with your password

@pytest.fixture(scope="function")
def server():
    """
    Fixture to connect to the server via SSH, start the iperf server, and clean up afterward.
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        # Start iperf server
        stdin, stdout, stderr = client.exec_command('iperf -s -D')
        yield stdout.read().decode(), stderr.read().decode()
    finally:
        # Stop iperf server
        client.exec_command('pkill -f iperf')
        client.close()

@pytest.fixture(scope="function")
def client(server):
    """
    Fixture to run iperf client and return the output and error for parsing.
    """
    try:
        # Run iperf client
        result = subprocess.run(
            ['iperf', '-c', SERVER_IP],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return None, str(e)

