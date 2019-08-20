import os
import random
path = './dataset'
file_list = os.listdir(path)

for file_name in file_list: 
	old_name = os.path.join(path, file_name)
	new_name = os.path.join(path, str(random.randint(10,99999)))
	os.rename(old_name, new_name)
