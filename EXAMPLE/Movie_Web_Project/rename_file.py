import os

def rename_files(path):
	# Get files name by list
	file_list = os.listdir(path)
	print file_list
	## After os.listdir(), the pwd has changed.
	# now_path = os.getcwd()
	# print now_path
	os.chdir(path)
	for file_name in file_list:
		print file_name
		os.rename(file_name, file_name.translate(None, '0123456789'))
		print file_name

rename_files('prank/')