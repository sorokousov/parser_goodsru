import pysftp

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    sftp.