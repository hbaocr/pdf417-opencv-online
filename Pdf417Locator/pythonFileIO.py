import os
import tempfile

def get_pwd():
    # detect the current working directory and print it
    return os.getcwd()

def create_dir(dir_path):
    directory = os.path.dirname(dir_path)
    if not os.path.exists(dir_path):
        try:
            # define the access rights in octext ( 0o prefix)
            access_rights = 0o755
            os.mkdir(directory,access_rights)
        except OSError:
            return 0
        else:
            return 1
    return 0

def del_dir(dir_path):
    directory = os.path.dirname(dir_path)
    if not os.path.exists(dir_path):
        try:
            os.rmdir(directory)
        except OSError:
            return 0
        else:
            return 1

def create_temp_dir():
    # create a temporary directory. Outside "with" ==> dir will be deleted
    with tempfile.TemporaryDirectory() as directory:
        print('The created temporary directory is %s' % directory)


#/var/folders/tw/nb59l3gx7zbfvbmnh0tf_99m0000gn/T/tmp717l7k3u

#create_temp_dir()