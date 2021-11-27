import shutil
import os
import sys

num_args = len(sys.argv)

if num_args == 1:
    raise ValueError('Please pass the directory name')
elif num_args > 2:
    raise ValueError("Can not parse directory name")

dir_name = sys.argv[1]
dir_path = os.path.join(os.getcwd(), dir_name)
shutil.make_archive(dir_path, 'zip', os.getcwd(), dir_name)