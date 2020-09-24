####################################
# File name: Menu.py               #
####################################

import cowsay
import ImageEncoding
import ImageDecoding
import Compare

cowsay.stegosaurus("Steg-Tool")
#Basic Menu
def menu():
    strs = ('Please Select From the following menu:\n'
            '\t1.) Embed a Secret Message into Local Image\n'
            '\t2.) Retrieve a Secret Message from a Local Image\n'
            '\t3.) Compare Images\n'
            '\t4.) Embed a Secret Message into a Remote Image\n'
            '\t5.) Retrieve a Secret Message from a Remote Image\n'
            '\t6.) Get Quantity of Images in Database\n'
            '\t7.) Exit\n')
    loop = True
    while(loop):
        choice = raw_input(strs)
        try:
            val = int(choice)
            loop = False
        except ValueError:
            print("")
            print("\nThat's not a number!")
            print("")
            loop = True
    return val

#Flow of Control
while True:
    choice = menu()
    if choice == 1:
        ImageEncoding.selectLocalImage()
    elif choice == 2:
        ImageDecoding.selectLocalImage()
    elif choice == 3:
        Compare.compare()
    elif choice == 4:
        ImageEncoding.selectImage()
    elif choice == 5:
        ImageDecoding.SelectImage()
    elif choice == 6:
        ImageEncoding.getQuantity()
    elif choice == 7:
        break
    else:
        True
        break

