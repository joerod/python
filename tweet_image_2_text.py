import tweepy
from urllib.parse import urlparse
import cv2
import pytesseract
import requests
import shutil
import os

def get_tweet_image(url):
    tweet_id = urlparse(url).path.split('/')[-1]
    access_token = ""
    access_token_secret = ""
    consumer_key=""
    consumer_secret=""
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    tweet_return = api.get_status(tweet_id,tweet_mode='extended')._json
    return tweet_return['entities']['media'][0]['media_url_https']

def download_image(image_url):    
    filename = image_url.split("/")[-1]
    r = requests.get(image_url, stream = True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return filename
    else:
        print('Image Couldn\'t be retreived')

def clean_up(file_path):
    os.remove(file_path)

def image2txt(location,outfile=None):
	# Read image from which text needs to be extracted
	img = cv2.imread(location)

	# Preprocessing the image starts

	# Convert the image to gray scale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Performing OTSU threshold
	ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

	# Specify structure shape and kernel size.
	# Kernel size increases or decreases the area
	# of the rectangle to be detected.
	# A smaller value like (10, 10) will detect
	# each word instead of a sentence.
	rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

	# Applying dilation on the threshold image
	dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

	# Finding contours
	contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	# Creating a copy of image
	im2 = img.copy()

	# A text file is created and flushed
	if outfile:
		file = open(outfile, "w+")
		file.write("")
		file.close()

	# Looping through the identified contours
	# Then rectangular part is cropped and passed on
	# to pytesseract for extracting text from it
	# Extracted text is then written into the text file
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		
		# Drawing a rectangle on copied image
		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		# Cropping the text block for giving input to OCR
		cropped = im2[y:y + h, x:x + w]
		
		# Open the file in append mode
		if outfile:
			file = open(outfile, "a")
		
		# Apply OCR on the cropped image
		text = pytesseract.image_to_string(cropped)
		print(text)

		# Appending the text into file
		if outfile:
			file.write(text)
			file.write("\n")
			
			# Close the file
			file.close

image = get_tweet_image('https://twitter.com/driscollis/status/1496100997621497864')
filename = download_image(image)
image2txt(os.path.join(os.getcwd(),filename))  
clean_up(filename)	
