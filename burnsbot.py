import os,json, re
import time
from slackclient import SlackClient
import markovify

###########  Functions for poem generation ###########
def load_model():
	"""
	Load the markov chain model for text generation. 
	Should be called at startup.
	"""
	with open('./markov_model.json', 'r') as f:
		model_json = json.load(f)

	markov_model = markovify.Text.from_json(model_json)
	return markov_model

def write_poem(n_lines):
	poem = []

	for line in range(n_lines):
		poem.append(new_line())
	return poem

def new_line():
	l = markov_model.make_short_sentence(60)
	if l!=None:
		return l
	else:
		l=new_line()
		return l

def print_poem(poem):
	return '\n'.join(poem)



########### Setup for Slack bot ###########

# burnsbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "write"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


########### Functions for parsing Slack output ##########


def handle_command(command, channel):
	"""
		Receives commands directed at the bot and determines if they
		are valid commands. If so, then acts on the commands. If not,
		returns back what it needs for clarification.
	"""
	response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
			   "* command with the number of lines of poetry that you'd like"
	
	if EXAMPLE_COMMAND in command:
		
		n_list = re.findall(r'\d+', command)
		
		if len(n_list) != 0:
			n_lines = int(n_list[0])
			pm = write_poem(n_lines)
			response = print_poem(pm)
		else:
			response = " How many lines of poetry would you like? You didn't specify!"
		
	slack_client.api_call("chat.postMessage", channel=channel,text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
	"""
	The Slack Real Time Messaging API is an events firehose.
	this parsing function returns None unless a message is
	directed at the Bot, based on its ID.
	"""
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				# return text after the @ mention, whitespace removed
				return output['text'].split(AT_BOT)[1].strip().lower(), \
				output['channel']
	return None, None




# Load up saved model
markov_model = load_model()

# Make the connection to Slack
if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print("StarterBot connected and running!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")