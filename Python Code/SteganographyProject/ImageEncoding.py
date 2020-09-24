####################################
# File name: ImageEncoding.py      #
####################################

from PIL import Image
import PIL.Image as Image
import hashlib
import random, string, base64
from Crypto.Cipher import AES
import os
import requests
import base64
import warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Retrieves Token from spring boot server
def getToken(h):
    print("")
    print("Getting Token from Server...")
    print("")
    url = "https://localhost:8443/token"
    headers = {'content-type': 'application/json'}
    payload = "{\n\t\"userName\": \"%s\",\n\t\"id\": 1,\n\t\"role\": \"admin\"\n}"
    response = requests.request("POST", url, data=payload % (str(h)), headers = headers, verify=False)
    if response.text != "Error":
        print("Token: ")
        print(response.text)
        return (response.text)
    else:
        print("Not Authorized...")
        print(response.text)
        return response.text


#Retrieves number of images on the spring boot server
def getImageCount(token):
    url = "https://localhost:8443/rest/images/"
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Token {}'.format(token)
    }
    response = requests.request("GET", url, data=payload, headers=headers, verify=False)
    return response.text

#Choose an image from the current directory, select a secret message and create a key/seed
def selectLocalImage():
        loop = True
        while(loop) :
            print("Select an Image")
            f = raw_input("Please type in the path to your file and press 'Enter': ")
            try:
                file = open(f, 'rb')
                print("")
                print "\tValid image selected"
                print("")
                loop = False
            except IOError:
                print("")
                print "\tCould not open/read file:", f
                print("")
                return


        original_image_file = file.name
        img = Image.open(original_image_file)
        encoded_image_file = "Encoded_" + original_image_file

        g = raw_input("Enter your Secret Message: ")
        message = g.encode()

        h = raw_input("Enter your Key: ")

        print("SHA-256 on key...")
        hash_object = hashlib.sha256(h)
        hex_dig = hash_object.hexdigest()
        mystring = str(hex_dig)
        print("Hash: " + mystring)
        print("Splitting key...")
        hashedKey = mystring[0:16]
        print("Hashed Key for AES: " + hashedKey)
        seed = mystring[16:32]
        print("IV and PRNG Seed: " + seed)

        iv = seed
        print("")
        print("Encrypting secret message...")
        enc_s = AES.new(hashedKey, AES.MODE_CFB, iv)
        cipher_text = enc_s.encrypt(message)
        print("\tEncrypted ciphertext: " + cipher_text)
        encoded_cipher_text = base64.b64encode(cipher_text)
        print("\tBase 64 encoded ciphertext: " + encoded_cipher_text)

        img_encoded = encode(img, encoded_cipher_text, seed)
        if img_encoded:
            img_encoded.save(encoded_image_file)
            print(" ")
            print("{} saved!".format(encoded_image_file))
            print(" ")
            os.startfile(encoded_image_file)

#Select an image from the current directory, embed a message, select key/seed and send it to the spring boot server
def selectImage():
    loop = True
    while (loop):
        print("Select an Image")
        f = raw_input("Please type in the path to your file and press 'Enter': ")
        try:
            file = open(f, 'rb')
            print("")
            print "\tValid image selected"
            print("")
            loop = False
        except IOError:
            print("")
            print "\tCould not open/read file:", f
            print("")
            return
    original_image_file = file.name

    img = Image.open(original_image_file)
    encoded_image_file = "enc_" + original_image_file

    g = raw_input("Enter your Secret Message: ")
    message = g.encode()

    loop = True
    while loop:
        h = raw_input("Enter your Key: ")
        token = getToken(str(h))
        if token == "Error":
            loop = True
        else:
            loop = False

    if token:
        print("SHA-256 on key...")
        hash_object = hashlib.sha256(h)
        hex_dig = hash_object.hexdigest()
        mystring = str(hex_dig)
        print("Splitting key...")
        hashedKey = mystring[0:16]
        print("Hashed Key: " + hashedKey)
        seed = mystring[16:32]
        print("IV and PRNG Seed: " + seed)
        iv = seed
        print("")
        print("Encrypting secret message...")
        enc_s = AES.new(hashedKey, AES.MODE_CFB, iv)
        cipher_text = enc_s.encrypt(message)
        print("\tEncrypted ciphertext: " + cipher_text)
        encoded_cipher_text = base64.b64encode(cipher_text)
        print("\tASCII of ciphertext: " + encoded_cipher_text)

        img_encoded = encode(img, encoded_cipher_text, seed)
        if img_encoded:
            img_encoded.save(encoded_image_file)
            print(" ")
            with open(encoded_image_file, "rb") as imageFile:
                imageString = base64.b64encode(imageFile.read())

            imageCount = str(int(getImageCount(token)) + 1)
            url = "https://localhost:8443/rest/images/" + imageCount + ""

            payload = "{\n\t\"id\": %d,\n\t\"image\": \"%s\"\n}"
            headers = {
                'Content-Type': "application/json",
                'Authorization': 'Token {}'.format(token)
            }

            response = requests.request("PUT", url, data=payload % (int(imageCount), imageString), headers=headers, verify=False)
            if response.status_code == 200:
                newimageCount = getImageCount(token)
                print("Image Number " + newimageCount + " Posted To Database")
                print("")
            else:
                print("Image Not Posted")
                print("")
    else:
        selectImage()

#Hide the message into the image randomly with the use of a seed
def encode(img, msg, seed):
    length = len(msg)
    if length > 255:
        print("text too long! (don't exeed 255 characters)")
        return False
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    print"Converting secret message to binary..."
    data = ''.join(format(ord(i), '08b') for i in msg)
    print("\tBinary: " + data)
    res = [int(i) for i in list('{0:0b}'.format(length))]

    loop = True
    while loop:
        if len(res) < 8:
            res.insert(0,0)
            loop = True
        else:
            loop = False

    res.append(0)

    encoded = img.copy()
    width, height = img.size
    print("")
    print("Embedding secret message size into image...")
    print("\tMessage is: " + str(len(msg)) + " bytes" + " / " + str(len(msg) * 8) + " bits")
    i = 0
    for x in range(0,3):
        pixel = list(img.getpixel((x, 0)))
        for n in range(0, 3):
            pixel[n] = pixel[n] & ~1 | int(res[i])
            i += 1
        encoded.putpixel((x, 0), tuple(pixel))
    j = 0
    loop = True
    a = random.seed(seed)
    print("Generating Random Values from seed...")
    print(" ")
    print("Hiding Cipher Text in Random Pixels...")
    while loop == True:
        x = random.randint(4, width - 1)
        y = random.randint(0, height - 1)
        pixel = list(img.getpixel((x, y)))
        for n in range(0, 3):
            if (j < len(data)):
                pixel[n] = pixel[n] & ~1 | int(data[j])
                j += 1
            else:
               loop = False
               break
        encoded.putpixel((x, y), tuple(pixel))
    return encoded

#Get the amount of images stored in the database and print the result to the console
def getQuantity():
    h = raw_input("Enter your Key: ")
    token = getToken(str(h))
    imageCount = str(int(getImageCount(token)))
    print("")
    print("\tThere are %s image(s) stored in the database" % imageCount)
    print("")

