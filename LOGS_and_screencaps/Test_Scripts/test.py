
from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC2e6db23c9db4517bbc226916c805c228"
auth_token  = "738cb95c13c339b5764253a2cb5d4933"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(body="u r a bitch nigga",
        to="+12483205295",
        from_="+12482138764")
print(message.sid)
