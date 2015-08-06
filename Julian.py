from WordSearch import WordSearch
from PIL import Image, ImageFont, ImageDraw
import tweepy
from time import sleep


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

font = font = ImageFont.truetype("montserrat/Montserrat-Regular.otf", 60)
thinfont = ImageFont.truetype("montserrat/Montserrat-Hairline.otf", 32)
dimensions = (2000,2000)
margin = dimensions[0]/8
square = (dimensions[0] - 2*margin) / 11


poem = [i.rstrip().split(" ") for i in open("poem.txt").readlines()]
poems = [i.rstrip().split(" ") for i in open("poem.txt").readlines()]

wsearches = []
for tweets in poem:
	wsearches.append( WordSearch(11, False, tweets) )

i = 0
while i<len(wsearches):
	wsearches[i].fill(len(poems[i]))
	i+=1

k = 0
for ws in wsearches:
	paper = Image.new("RGBA",dimensions, "#FFF")
	draw = ImageDraw.Draw(paper)
	draw.text( (800, 1900), '@DastardlyEpic', (128,128,128), thinfont)

	for i in range(0,11):
		for j in range(0,11):
			if(ws.board_available[i][j]):
				col = (0,0,0)
			else:
				col = (255,57,30)

			if(ws.board[i][j] == "I"):
				draw.text( ( (margin+i*square) + 15, margin+j*square), ws.board[i][j], col, font)
			else:
				draw.text( (margin+i*square, margin+j*square), ws.board[i][j], col, font)

	resize = paper.resize((dimensions[0]/5,dimensions[1]/5), Image.ANTIALIAS)
	paper.save("WS/%d.png" % k, "PNG")
	k+=1

for i in range(0,25):
	api.update_with_media("WS/%d.png"%i, (" ").join(poems[i]))
	sleep(180)