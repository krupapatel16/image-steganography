# image-steganography

Ever increasing privacy concerns and sharing of data exacerbate the need to hide data in a secure method.
To fool others from looking at your communications, this concept is used as a “hidden in plain sight” approach.
In this project I demonstrate a method to encrypt a message inside an image, throw off those trying to decode it, and use an alternate form of LSB information hiding without 
showing a drastic change in the image.

Structure Of the Project

1. Image Encoding Embed a secret message into a local image
2. Image Decoding Retrieve a secret message from a local image
3. Compare hash value of an original image with the encoded image
4. Embed a secret message into an image and send to it to a server
securely
5. Securely retrieve a secret message from a remote image on a
server
