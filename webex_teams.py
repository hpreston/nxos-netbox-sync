from webexteamssdk import WebexTeamsAPI
import os

if "TEAMS_TOKEN" in os.environ.keys() and "TEAMS_ROOMID" in os.environ.keys():
    token = os.environ["TEAMS_TOKEN"]
    roomid = os.environ["TEAMS_ROOMID"]
else: 
    token = None 
    roomid = None
    print("No details for sending Teams messages found. Add ENVVARS to use these features.")

def notify_team(message):
    """Simple function to send a Teams message. Requires ENV to be set for token and room."""
    if token and roomid: 
        try:
            teams = WebexTeamsAPI(access_token = token)
            send = teams.messages.create(roomid, markdown = message)
            return True

        except Exception as e:
            return False
    else: 
        print("Unable to send message")
        return False 