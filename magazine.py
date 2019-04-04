#imports
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps 
import pytesseract
import argparse
import cv2
import os
import numpy as np
import pandas as pd
import re


#initialize dataframe
mag_df = pd.DataFrame(columns = ['pub_date','cov_text'])  


#open file with all cover info
#pdf = PyPDF2.PdfFileReader(open('/Users/noramay/Downloads/cover_test.pdf', "rb"))
#num_of_pages = pdf.getNumPages()
for i in range(780,785):
	dir = '/Users/noramay/desktop/AllZips/Folder{}/'.format((i+1))
	list = os.listdir(dir) # dir is your directory path
	number_files = len(list)
	text_one_issue = ''
	imagefile = '/Users/noramay/desktop/AllZips/Folder{}/image1.jpg'.format((i+1))

	#run a function that returns all text (both ways of processing) for now, just have full function text in here?
	# load the image and convert it to grayscale
	image = cv2.imread(imagefile)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#apply thresholding to preprocess
	gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
	gray = cv2.bilateralFilter(gray,9,75,75)
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	text_one_issue = text_one_issue + ' ' + text

	#CV same with inverted image
	img = Image.fromarray(image)  # RGB image
	gray = ImageOps.invert(img)
	gray = np.array(gray)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	gray = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]
	gray = cv2.bilateralFilter(gray,9,75,75)
 
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	text_one_issue = text_one_issue + ' ' + text

	issue_date = re.findall(r'(\w+ \d{4})', text_one_issue)
	df2 = pd.DataFrame({'pub_date':[issue_date],'cov_text':[text_one_issue]})
	mag_df = pd.concat([mag_df,df2], ignore_index=True)
	print(i)
import pickle
mag_df.to_pickle('mar18_4.pkl')   
