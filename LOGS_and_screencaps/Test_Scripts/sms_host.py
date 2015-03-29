from flask import Flask, request, redirect
import twilio.twiml
import paramiko
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)
    r = twilio.twiml.Response()
    if body == 'hello':
        r.message("Hi!")
    elif body == 'mkdir':
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('35.14.109.168', username='root', password='legendaryheroes')
        stdin, stdout, stderr = client.exec_command("mkdir ssh_test")
        r.message('directory created')
    else:
        r.message(body)
    return str(r)


 
if __name__ == "__main__":
    app.run(debug=True)

