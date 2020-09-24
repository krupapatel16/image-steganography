####################################
# File name: Compare.py            #
####################################

from PIL import Image
import imagehash

#Basic Comparison, will need more indepth analysis
#TODO: Test the cutoff level with different images to find any false positives
def compare():
    print("Select the first Image")
    f = raw_input("Please type in the path to your file and press 'Enter': ")
    file1 = open(f, 'r')

    print("Select the second Image")
    f2 = raw_input("Please type in the path to your file and press 'Enter': ")
    file2 = open(f2, 'r')

    hash0 = imagehash.average_hash(Image.open(file1.name))
    hash1 = imagehash.average_hash(Image.open(file2.name))
    cutoff = 1

    if hash0 - hash1 < cutoff:
        print("")
        print(hash0)
        print(hash1)
        print('Images hashes are similar')
        print("")
    else:
        print("")
        print(hash0)
        print(hash1)
        print('Images hashes are not similar')
        print("")




