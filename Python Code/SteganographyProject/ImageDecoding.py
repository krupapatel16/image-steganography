####################################
# File name: ImageDecoding.py      #
####################################

from PIL import Image
import PIL.Image as Image
import hashlib
import random, string, base64
from Crypto.Cipher import AES
import os
import binascii
import math
import requests

#Retrieves Token from spring boot server
def getToken(h):
    url = "https://localhost:8443/token"
    headers = {'content-type': 'application/json'}
    payload = "{\n\t\"userName\": \"%s\",\n\t\"id\": 1,\n\t\"role\": \"admin\"\n}"
    response = requests.request("POST", url, data=payload % (str(h)), headers = headers, verify=False)
    print("Token: ")
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

#Retrieve the converted image from the server
def getResponse(token, indexnumber):
    url = "https://localhost:8443/rest/images/" + indexnumber
    payload = ""
    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Token {}'.format(token)
    }
    response = requests.request("GET", url, data=payload, headers=headers, verify=False)

    return response

decimal = 0

#Retrieve a hidden message from the image using the prng and same seed as before
def decode(img2, seed):
    print("Revealing Cipher Text...")
    width, height = img2.size
    extracted_bin = []
    width, height = img2.size
    byte = []
    print("Extracting the size of the message...")
    for x in range(0, 3):
        pixel = list(img2.getpixel((x, 0)))
        for n in range(0, 3):
            extracted_bin.append(pixel[n] & 1)
            data3 = "".join([str(x) for x in extracted_bin])
    global decimal
    decimal = int(data3[0:-1],2)
    maxRange = int(math.ceil((decimal * 8) /3))
    messageLength = (decimal * 8) + 9
    print("\tSize: " + str(messageLength/8) + " bytes / " + str(messageLength) +  " bits")
    loop = True
    a = random.seed(seed)
    j = 0
    while loop == True:
        for x in range(0, maxRange+1):
            x = random.randint(4, width - 1 )
            y = random.randint(0, height - 1)
            pixel = list(img2.getpixel((x, y)))
            for n in range(0, 3):
                extracted_bin.append(pixel[n] & 1)
        else:
            loop = False
            break
    data = "".join([str(x) for x in extracted_bin])
    return data

file2 = ""

#Choose an image from the current directory, and retrieve the hidden message
def selectLocalImage():
    loop = True
    while (loop):
        print("Select an Image")
        f = raw_input("Please type in the path to your file and press 'Enter': ")
        if (f.startswith("Encoded_")):
            try:
                file2 = open(f, 'rb')
                print("")
                print "\tValid image selected"
                print("")
                loop = False
            except IOError:
                print("")
                print "\tCould not open/read file:", f
                print("")
                loop = True
        else:
                print("")
                print("\tNot an altered image")
                print("")
                return

        encoded_image_file = file2.name

        img2 = Image.open(encoded_image_file)

        h = raw_input("Enter your Key: ")

        hash_object = hashlib.sha256(h)
        hex_dig = hash_object.hexdigest()
        mystring = str(hex_dig)
        print("Splitting key...")
        hashedKey = mystring[0:16]
        print("Hashed Key: " + hashedKey)
        seed = mystring[16:32]
        print("IV and PRNG Seed: " + seed)
        iv = seed
        hidden_text = decode(img2, seed)

        messageLength = (decimal * 8) + 9

        messageLength = (decimal * 8) + 9

        data2 = hidden_text[9:messageLength]
        n = int(str(data2), 2)
        print("Extracted binary: " + data2)
        encodedText = binascii.unhexlify('%x' % n)
        print("Binary to ASCII: " + encodedText)
        print("Hex value base64 decoded: " + base64.b64decode(encodedText))
        decryption_suite = AES.new(hashedKey, AES.MODE_CFB, iv)
        plain_text = decryption_suite.decrypt(base64.b64decode(encodedText))

        print("")
        print("Decrypted Secret Message:")
        print(plain_text)
        print("")

userIndex = ""
#Enter the index of the image saved on the sever and retrieve the image, enter the key, and decode the secret message
def SelectImage():
    global userIndex
    loop = True
    while (loop):
        try:
            h = raw_input("Enter your Key: ")
            token = getToken(h)
            if(token == "Error"):
                loop = False
            loop = False
        except ValueError:
            print "Enter a Number..."
            loop = True

    imageCount = int(getImageCount(token))
    loop2 = True
    while (loop2):
        try:
            userIndex = raw_input("Enter image index:")
            if userIndex < imageCount:
                print("not valid")
            loop2 = False
        except ValueError:
            print "Enter a Number..."
            loop2 = True

    myResponse = getResponse(token, str(userIndex))
    data = myResponse.json()
    if(data != 0):
        image = data["image"]
        print(" ")
        print("Recieved Image from Database...")
        print(" ")

        fh = open("imageToSave.png", "wb")
        fh.write(image.decode('base64'))
        fh.close()

        img2 = Image.open("imageToSave.png")

        os.startfile("imageToSave.png")

        hash_object = hashlib.sha256(h)
        hex_dig = hash_object.hexdigest()
        mystring = str(hex_dig)
        hashedKey = mystring[0:16]
        seed = mystring[16:32]
        iv = seed
        hidden_text = decode(img2,seed)
        messageLength = (decimal * 8) + 9

        messageLength = (decimal * 8) + 9

        data2 = hidden_text[9:messageLength]
        n = int(str(data2), 2)
        print("\tExtracted binary: " + data2)
        encodedText = binascii.unhexlify('%x' % n)
        print("\tBinary to hex: " + encodedText)
        print("\tHex value base64 decoded: " + base64.b64decode(encodedText))
        decryption_suite = AES.new(hashedKey, AES.MODE_CFB, iv)
        plain_text = decryption_suite.decrypt(base64.b64decode(encodedText))

        print("")
        print("Decrypted Secret Message:")
        print(plain_text)
        print("")
    else:
        print("")
        print("No Images In Database")
        print("")


