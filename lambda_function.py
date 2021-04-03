
import boto3
import paramiko
def s3_deploy(event, context):

    #User Input
    SSH_File_Bucket="document-upload-elasticsearch"
    SSH_Key_Name="keys/Haystack.pem"
    Server_SSH_KeyLocation="keys/Haystack.pem"
    HOST="18.232.38.209"
    #Replace s3://dummy-bucket-test-aa with actual bucket name
    #Replace /path/dest/dir with actual local directory  
    #Replace login username ubuntu to actual username

    s3 = boto3.resource('s3')
    #Download private key file from secure S3 bucket
    s3.meta.client.download_file(SSH_File_Bucket, SSH_Key_Name, Server_SSH_KeyLocation)

    k = paramiko.RSAKey.from_private_key_file(Server_SSH_KeyLocation)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("Connecting to " + HOST)
    c.connect( hostname = HOST, username = "root", pkey = k )
    print("Connected to " + HOST)

    commands = [
        "sudo aws s3 sync s3://document-upload-elasticsearch /root/haystack/data/story","pwd"]
    for command in commands:
        print("Executing {}".format(command))
        stdin , stdout, stderr = c.exec_command(command)
        print(stdout.read())
        print(stderr.read())

    return
    {
        'message' : "Script execution completed. See Cloudwatch logs for complete output"
    }
