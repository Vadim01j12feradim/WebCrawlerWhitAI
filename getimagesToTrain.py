import requests
from bs4 import BeautifulSoup
import cv2
import cairosvg
from io import BytesIO
from PIL import Image
import numpy as np
import os
import shutil
import time
def showImage(url,yOrNot):
            try:

                extension = url.split(".")[-1]
                path = 'Images/'+yOrNot  # Reemplazar con la ruta de la carpeta que deseas analizar
                num = 0

                # Iterar sobre los nombres de archivo en la carpeta
                for file_name in os.listdir(path):
                    num += 1  # Incrementar el contador de archivos
                num += 1
                print(f'La carpeta "{path}" contiene {num} archivos.')

                if extension.lower() == "svg":
                    out = str(num)+".png"
                    cairosvg.svg2png(url=url, write_to=out)
                    image = cv2.imread(out, cv2.IMREAD_UNCHANGED)
                    height, width, channels = image.shape
                    print(f"Width: {width}, Height: {height}")
                else:
                    response = requests.get(url)
                    image_data = BytesIO(response.content)
                    # Open the image using PIL
                    image = Image.open(image_data)
                    width, height = image.size
                    # Display the image using matplotlib
                    # plt.imshow(image)
                    # plt.show()
                    # plt.close()
                    if extension.lower() != "gif":
                        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                # Display the image using cv2.imshow()
                cv2.imshow("Image", image)
                print('Images.'+extension.lower())
                cv2.imwrite('Images/'+yOrNot+'/'+str(num)+'.jpg', image)

                # Wait for a key press
                cv2.waitKey(200)

                # Close all OpenCV windows
                cv2.destroyAllWindows()
            except Exception as e:
                 print("Has error in image file")
def search(theme,url,yOrNot):
    # Query parameters for the API request
    params = {
        "q": theme,
        "qft": "+filterui:photo-photo",
        "FORM": "HDRSC2"
    }
    try:

        # Send GET request to Bing Image Search API
        response = requests.get(url, params=params)
        # time.sleep(7)
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            links = soup.find_all('a')
            image_urls = []
                            
            path = 'Images/yes'  # Reemplazar con la ruta de la carpeta que deseas analizar
            num = 0

            # Iterar sobre los nombres de archivo en la carpeta
            for file_name in os.listdir(path):
                num += 1  # Incrementar el contador de archivos
            num += 1
            print(f'La carpeta "{path}" contiene {num} archivos.')

            path = 'Images/no'  # Reemplazar con la ruta de la carpeta que deseas analizar
            numN = 0

            # Iterar sobre los nombres de archivo en la carpeta
            for file_name in os.listdir(path):
                numN += 1  # Incrementar el contador de archivos
            numN += 1
            print(f'La carpeta "{path}" contiene {numN} archivos.')

            for img in soup.find_all('img',src=True):
                image_url = img['src']
                # if image_url == "https://lh3.google.com/u/0/d/1BNYX-AuV8mH8duH0I3NuWGo5AV6DDDHJ=w200-h190-p-k-nu-iv2":
                #      while True:
                #         print("*")
                if not image_url.startswith("http://") and not image_url.startswith("https://"):
                    # Add default scheme
                    image_url = "https:" + image_url
                if(numN+len(image_urls) >= num and yOrNot == "no"):
                    break
                image_urls.append(image_url)
            if image_urls:
                print(f'Image URLs for "{theme}":')
                for image_url in image_urls:
                    print("\t",image_url)
                    showImage(image_url,yOrNot)

            else:
                print(f'No Videos found for "{theme}".')
        else:
            print('Failed to fetch image URLs.')
    except Exception as e:
    # handle the exception
        print(f"An error occurred: {e}")
def setArrayUrls(theme,yesOrNot):
    searchs = np.array([
         "https://www.dogpile.com/serp?qc=images&q="+theme.replace(" ", "+")+"&sc=RYQ4ycEI0Jfg10",
         "https://www.qwant.com/?t=images&q="+theme.replace(" ", "+"),
         "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="+theme.replace(" ", "+"),
         "https://www.ecosia.org/images?q="+theme.replace(" ", "+"),
         "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1682976195641_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCw2LDIsMywxLDQsNSw3LDgsOQ%3D%3D&ie=utf-8&sid=&word="+theme.replace(" ", "+"),
         "https://www.google.com/search?q="+theme.replace(" ", "+")+"&tbm=isch&ved=2ahUKEwjxibfhkND-AhWXKN4AHTiiCVQQ2-cCegQIABAA&oq="+theme.replace(" ", "+")+"&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyCAgAEIAEELEDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEIoFEEM6BggAEAUQHjoHCAAQGBCABDoLCAAQgAQQsQMQgwFQnQdYvAxgqw1oAHAAeACAAcIBiAH4BpIBAzMuNJgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=BZlNZLHzJJfR-LYPuMSmoAU&bih=968&biw=1920&client=ubuntu&hs=fVc",
         "https://search.aol.com/aol/image;_ylt=Awrih0Xll01kyUsiESFpCWVH;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?q="+theme.replace(" ", "+")+"&s_it=searchtabs&v_t=comsearch",
         "https://yandex.com/images/search?from=tabbar&text="+theme.replace(" ", "+"),
         "https://mx.images.search.yahoo.com/search/images;_ylt=AwrEtWqulE1kJCAiCSPD8Qt.;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p="+theme.replace(" ", "+")+"&fr2=piv-web&fr=yfp-t",
         "https://www.bing.com/images/search"])
    print(searchs)

    # i = 0
    for j in range(searchs.shape[0]):
        # i = 
        search(theme, searchs[j],yesOrNot)

def searchData(theme,yesOrNot):
    if(yesOrNot == "yes"):
        shutil.rmtree('Person')
        shutil.rmtree('Images/yes')
        os.mkdir('Person')
        os.mkdir('Images/yes')
        setArrayUrls(theme,yesOrNot)
    else:
        shutil.rmtree('Images/no')
        os.mkdir('Images/no')
        setArrayUrls("icons",yesOrNot)
        setArrayUrls("text",yesOrNot)



    # Bing Image Search API endpoint
    # url = "https://duckduckgo.com/?q="+theme+"&t=h_&iar=images&iax=images&ia=images"
    

    # i = search(theme, url, 0)
    # url = "https://www.bing.com/images/search"
    # i = search(theme, url, i+1)
    # url = "https://www.google.com/search?q="+theme+"&source=lnms&tbm=isch&sa=X&ved=2ahUKEwigpNH9zb7-AhXIM0QIHWGgAn0Q_AUoAXoECAEQAw&biw=1440&bih=727&dpr=1.33"
    # search(theme, url,i+1)
# searchData("icons","no")
# searchData("text","no")
