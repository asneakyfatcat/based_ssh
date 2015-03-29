__author__ = 'Charles Moshier'
########################################################################################################################
#                                                                                                                      #
# This is a proof of concept python script using the Twilio API to enable control of hardware or software devices via  #
# SMS messages.                                                                                                        #
#                                                                                                                      #
# The goal of this was to control hardware easily through SMS which was done by triggering scripts written             #
# in the arduino IDE on an Intel Edison. In the future I would like to flesh this project out and start moving towards #
# home automation. I also plan on moving away from SSH and towards scripts fetching SMS commands via databases.         #
#                                                                                                                      #
# SSH was only used as a proof of concept, it is a horrible idea to use it in this manner due to security. It was only #
# used because of the lack of time and the amount of time spent on Edison debugging.                                   #
#                                                                                                                      #
########################################################################################################################
#                                                                                                                      #
# SO HOW DOES IT WORK!?!?!?                                                                                            #
#                                                                                                                      #
# A python script sets up a flask server which constantly listens for incoming commands. The Twilio API and services   #
# send these commands via POST when a text is relieved or sent, the incoming post is sent from the flask server        #
# and processed through this python script which sends back POST to the api, along with commands to the intel Edison,  #
# or whatever device you are connecting to.                                                                            #
#                                                                                                                      #
# Side note: I also used the program ngrok for easy tunneling for the flask server.                                    #
#                                                                                                                      #
########################################################################################################################
#                                                                                                                      #
# Where to go now!?                                                                                                    #
#                                                                                                                      #
# -switch from SSH to database fetching for security and ease of use                                                   # #                                                                                                                      #
# -Add more commands and ease of use                                                                                   #
# -add comments explaining what the hell is going on                                                                   #
# -clean up code                                                                                                       #
# -splash screen when connecting for the first time                                                                    #                                               
# -!?!?!?!??!!?                                                                                                        #
# -profit                                                                                                              #
#                                                                                                                      #
########################################################################################################################

from flask import Flask, request, redirect
import twilio.twiml
import paramiko

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def listen():

    help = '''ssh help

    Example Command:
    ssh -p [port] user@host -pass password'''

    welcome = '''Welcome to based_sms, an sms based SSH portal. If you need help connecting just reply 'SSH --help'''

    ssh_port = 22
    user = ""
    host = ""
    passw = ""

    ###############################################################################################################

    body = request.values.get('Body', None)
    r = twilio.twiml.Response()
    cmnd_split = ((body.lower()).split(' '))

    if body.lower() == "--help":
        r.message(welcome)
        return str(r)

    elif body.lower() == "ssh --help":

        r.message(help)
        return str(r)



    ###############################################################################################################
    if cmnd_split[0] == 'ssh':
        if (len(cmnd_split) < 4) or (len(cmnd_split) > 6):
            r.message("ERROR in parameter length, see ssh --help for help")
            return str(r)

        if cmnd_split[1] == '-p':
            ssh_port = 22

        elif '@' in cmnd_split[1]:
            user_host = cmnd_split[1].split('@')
            user = user_host[0]
            host = user_host[1]
            passw = cmnd_split[3]

        if '@' in cmnd_split[3]:
            user_host = cmnd_split[3].split('@')
            user = user_host[0]
            host = user_host[1]
            if cmnd_split[4] == '-pass':
                passw = cmnd_split[5]
            else:
                r.message("ERROR in parameter, see ssh --help for help")
                return str(r)

        while 1:
            body = request.values.get('Body', None)
            r = twilio.twiml.Response()

            try:
               # print(host, user, passw)
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, username=user, password=passw)
                #stdin, stdout, stderr = client.exec_command("mkdir ayylmao")
                r.message('Connected to ',host,' as ',user, " type 'quit' to quit")
                stdin, stdout, stderr = client.exec_command(body)
                break
            except:
                r.message('Unexpected Error, Could Not Connect')
                break




        return str(r)

    else:
        r.message("INVALID COMMAND: if you need help connecting please type ssh --help")
        return str(r)



if __name__ == "__main__":
    app.run(debug=True)

