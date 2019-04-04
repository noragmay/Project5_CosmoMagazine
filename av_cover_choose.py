from __future__ import print_function
import numpy as np
import argparse
import json
import cv2

covers = []
count = 0
	# loop over the magazine issues belonging to the current decade
years = ['196']
months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

for month in months:
	for year in years:
		for i in range(0,785):
		
			filepath = ('/Users/noramay/desktop/AllZips/Folder{}/date.txt'.format((i+1)))
			fh = open(filepath,"r")
			date = str(fh.read())
			if month in date and year in date:
	# load the image
				imagefile = '/Users/noramay/desktop/AllZips/Folder{}/image1.jpg'.format((i+1))
				cover = cv2.imread(imagefile)

# resize the magazine cover, flatten it into a single
		# list, and update the list of covers
				cover = cv2.resize(cover, (400, 527)).flatten()
				covers.append(cover)
				count = count + 1
				print(count)

	# compute the average image of the covers then write the average
	# image to disk
avg = np.average(covers, axis=0).reshape((527, 400, 3)).astype("uint8")
p = "1960s.png"
cv2.imwrite(p, avg)
print(count)

