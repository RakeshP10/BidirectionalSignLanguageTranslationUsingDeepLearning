# Python 3 code to rename multiple
# files in a directory or folder

# importing os module
import os
import string
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

# Function to rename multiple files
def main(folder):

	
	for count, filename in enumerate(os.listdir(folder)):
		dst = f"t{str(count)}.jpg"
		src =f"{folder}/{filename}" # foldername/filename, if .py file is outside folder
		dst =f"{folder}/{dst}"
		
		# rename() function will
		# rename all the files
		os.rename(src, dst)

def main1(folder):

	
	for count, filename in enumerate(os.listdir(folder)):
		dst = f"{str(count)}.jpg"
		src =f"{folder}/{filename}" # foldername/filename, if .py file is outside folder
		dst =f"{folder}/{dst}"
		
		# rename() function will
		# rename all the files
		os.rename(src, dst)

# Driver Code
if __name__ == '__main__':

	for x in alphabet_list:
		folder = "dataSet/testingData/" + x
		main(folder)
		main1(folder)
	# Calling main() function
	
