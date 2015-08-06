from WordSearch import WordSearch
from PIL import Image, ImageFont, ImageDraw
import tweepy
from time import sleep


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)	
api = tweepy.API(auth)

font = font = ImageFont.truetype("montserrat/Montserrat-Regular.otf", 60)
thinfont = ImageFont.truetype("montserrat/Montserrat-Hairline.otf", 32)
#size of crossword image. Will be scaled by .2 to fix anti-aliasing issue
dimensions = (2000,2000)
margin = dimensions[0]/8
#The size of a letter in the wordsearch grid
square = (dimensions[0] - 2*margin) / 11

"""
Frustratingly, I couldn't figure out how to both use the list poem to fill() the wordsearches, 
(which pops() the words from the passed list to avoid reuse) and use it later as the text of 
the status updates. I had to settle for creating two lists. If anyone knows how to fix this,
or a good resource to learn about pythonic list objects, emaile me at vneck@uw.edu


Full credit for poem goes to Julian Epp (@BurntMayonaise). I wrote the code to baaaarly 
parse the text in the poem, leaving it to the user. This is an area of potenial future
improvement
"""

poem = [i.rstrip().split(" ") for i in open("poem.txt").readlines()]
poems = [i.rstrip().split(" ") for i in open("poem.txt").readlines()]

wsearches = []
for tweets in poem:
	wsearches.append( WordSearch(11, False, tweets) )

wslen = len(wsearches)

for i in range(0, wslen):
	wsearches[i].fill(len(poems[i]))

k = 0
for ws in wsearches:
	paper = Image.new("RGBA", dimensions, "#FFF")
	draw = ImageDraw.Draw(paper)
	#Watermark
	draw.text( (800, 1900), '@DastardlyEpic', (128,128,128), thinfont)

	for i in range(0,wslen):
		for j in range(0,wslen):
			if(ws.board_available[i][j]):
				"""board_available is a matrix with the same dimensions of the word search, 
				which records in a boolean whether a particular letter is part of a solution or not.
				"""
				col = (0,0,0)
			else:
				col = (255,57,30)

			#Had to include if statement to avoid bad kerning with the I's
			if(ws.board[i][j] == "I"):
				draw.text( ( (margin+i*square) + 15, margin+j*square), ws.board[i][j], col, font)
			else:
				draw.text( (margin+i*square, margin+j*square), ws.board[i][j], col, font)

	#Neccasary, for aesthetic reasons. Fixes antialiasing issue.
	resize = paper.resize((dimensions[0]/5,dimensions[1]/5), Image.ANTIALIAS)
	paper.save("WS/%d.png" % k, "PNG")
	k+=1

for i in range(0,25):
	api.update_with_media("WS/%d.png"%i, (" ").join(poems[i]))
	sleep(180)
	"""Twitter's API's rate limit for tweets is 15 status updates per 15 minute period. 
	This keeps well within that range.
	"""