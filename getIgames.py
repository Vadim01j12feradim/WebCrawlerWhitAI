import requests
from bs4 import BeautifulSoup
from PIL import Image

from io import BytesIO
import matplotlib.pyplot as plt
import base64
import io
import time
import cv2
import numpy as np
from urllib.parse import urljoin
import cairosvg
from moviepy.editor import VideoFileClip
import pygame
import sys
from selenium import webdriver
import moviepy.editor as mp
import os
# my files
import analiceFrame as an
import imghdr
import urllib.request as rq


# Bing Image Search API endpoint
# url = "https://www.bing.com/images/search"
class GetFiles(object):
        def __init__(
            self,
            url = "",
            typeFile = None, 
            theme = "",
            params = None
            ):  
                self.url = url #esta es la busqueda
                self.typeFile = typeFile
                self.theme = theme
                self.params = {
                "q": theme,
                "qft": "+filterui:photo-photo",
                "FORM": "HDRSC2"
                }
# url = "https://www.google.com/search?q=images&source=lnms&tbm=isch&sa=X&ved=2ahUKEwigpNH9zb7-AhXIM0QIHWGgAn0Q_AUoAXoECAEQAw&biw=1440&bih=727&dpr=1.33"
        
        def showVideo(self,url):
            # Load the video clip
            video = mp.VideoFileClip(url)
            video.preview()
        def showImage(self,url):
            # try:

                extension = url.split(".")[-1]
                yes = False
                if extension.lower() == "svg":
                    out = "drop.jpg"
                    cairosvg.svg2png(url=url, write_to=out)
                    image = cv2.imread(out, cv2.IMREAD_UNCHANGED)
                    yes = an.analize(image)
                    height, width, channels = image.shape
                    print(f"Width: {width}, Height: {height}")
                else:
                    
                    response = requests.get(url)
                    fyleType = imghdr.what(None, response.content)
                    print("Type of file is: ",fyleType)
                    if (fyleType == "gif"):
                        name = "temp.jpg"
                        response = requests.get(url, stream=True)
                        with Image.open(response.raw) as im:
                            im = im.convert('RGB')
                            im.save(name, "JPEG")
                        image = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                        yes = an.analize(image)
                        
                    if(fyleType == "jpeg" or extension.lower() == "jpg"):
                         name = "temp.jpeg"
                         rq.urlretrieve(url,name)
                         image = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                         yes = an.analize(image)
                    if(fyleType == "webp"):
                         name = "temp.jpeg"
                         img = Image.open(BytesIO(response.content))
                         imgToJpg = img.convert('RGB')
                         imgToJpg.save(name)
                         image = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                         yes = an.analize(image)
                    if(fyleType== "png"):
                        img = Image.open(BytesIO(response.content))
                        # Convert the image to JPEG format
                        img = img.convert('RGB')
                        name = 'temp.jpeg'
                        # Save the image as JPEG
                        img.save(name, 'JPEG')
                        image = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                        yes = an.analize(image)

                    

                    # image_data = BytesIO(response.content)
                    # # Open the image using PIL
                    # image = Image.open(image_data)
                    # img_array = np.array(image)

                    # # Extract the first frame from the array
                    
                    # frame = img_array[0,:,:,:]
                    # an.analize(frame)

                    # width, height = image.size
                    # if height <=32 and width <= 32:
                    #     return "This is a icon"
                    # # Display the image using matplotlib
                    # # plt.imshow(image)
                    # # plt.show()
                    # # plt.close()
                    # if extension.lower() != "gif":
                    #     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # Display the image using cv2.imshow()
                cv2.imshow("Image", image)

                # Wait for a key press
                cv2.waitKey(100)

                # Close all OpenCV windows
                cv2.destroyAllWindows()
                return yes
            # except Exception as e:
            #      print("Has error in image file")

            
            
        def search(self):
            # Query parameters for the API request
            # Send GET request to Bing Image Search API
            try:
                response = requests.get(self.url, params=self.params) 
                
                # Check if request was successful (status code 200)
                if response.status_code == 200:
                    # Parse HTML content
                    soup = BeautifulSoup(response.content, 'lxml')
                    # soup = BeautifulSoup(html, 'html.parser') # to convert

                    ############################## pdfs
                    # Find all the links on the webpage
                    links = soup.find_all('a')

                    # Create a directory to store the downloaded PDFs
                    if not os.path.exists('pdfs'):
                        os.mkdir('pdfs')

                    # Loop through all the links and download the PDFs
                    for link in links:
                        href = link.get('href')
                        if href.endswith('.pdf'):
                            filename = href.split('/')[-1]
                            filepath = os.path.join('pdfs', filename)
                            response = requests.get(href)
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                    # file_name = "example.txt"
                    # with open(file_name, "w") as file:
                    #     # Write your text to the file
                    #     file.write(str(soup))
                    # Extract image URLs from HTML img tags
                    ####################################### images
                    image_urls = []
                    for img in soup.find_all('img',src=True):
                        image_url = img['src']
                        # if image_url == "https://lh3.google.com/u/0/d/1BNYX-AuV8mH8duH0I3NuWGo5AV6DDDHJ=w200-h190-p-k-nu-iv2":
                        #      while True:
                        #         print("*")
                        if not image_url.startswith("http://") and not image_url.startswith("https://"):
                                # Add default scheme
                            image_url = "https:" + image_url
                        image_urls.append(image_url)
                    if image_urls:
                        print(f'Image URLs for "{self.theme}":')
                        for image_url in image_urls:
                            print("\t",image_url)
                            if(self.showImage(image_url)):
                                return True
                    else:
                        print(f'No Videos found for "{self.theme}".')
                    ########################## video
                    video_urls = []
                    for video in soup.find_all('video',src=True):
                        video_url = video["src"]
                        video_urls.append(video_url)
                    if video_urls:
                        print(f'Video URLs for "{self.theme}":')
                        for video_url in video_urls:
                            print("\t",video_url)
                            self.showVideo(video_url)
                    
                else:
                    print('Failed to fetch image URLs.')
                return False
            except Exception as e:
            #     # Manejo genérico para otras excepciones
                 print("Error:", e)

# url = "https://elcomercio.pe/resizer/SUXK3g7XhYu-3-eFKu43HhFdNrQ=/1200x1200/smart/filters:format(jpeg):quality(75)/cloudfront-us-east-1.images.arcpublishing.com/elcomercio/2EWGLS7445FJ5KXWGT75I5CPDE.jpg"
# GetFiles(url).showImage(url)