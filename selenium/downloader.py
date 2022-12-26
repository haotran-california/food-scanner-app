class Downloader:
    def __init__(self): 
        self.name = "something"

    def downloadImage(self, url, item, file_name): 
        try: 
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)

            file_path = f"./dataset/{item}/{file_name}"
            print(file_path)
            with open(file_path, "wb") as file: 
                image.save(file, "JPEG") 

        except Exception as e: 
            print("Failed Download:  ", e)

    def scrollDown(self): 
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def getImagesFromGoogle(self, url, delay, max_images, item):
        self.browser.get(url)
        imageURLSet = set()
        skips = 0

        print(f"PARSING THE {item} PHOTOS")
        self.scrollDown()       
        time.sleep(1)

        thumbnails = self.browser.find_elements(By.CLASS_NAME, "Q4LuWd") 
        n = len(thumbnails)
        print(f"FOUND {n} THUMBNAILS")
        
        for i in range(max_images): 
            thumbnail = thumbnails[i]
            thumbnail.click()
            time.sleep(delay)

            images = self.browser.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                imageSRC = image.get_attribute("src")
                if "http" in imageSRC: 
                     imageURLSet.add(imageSRC) 
            



        return imageURLSet
 
    def searchImageList(self, imageList):

        for item in imageList: 
            baseURL = "https://www.google.com"
            searchURL = baseURL + "/search?q=" + item
            self.browser.get(searchURL) 

            #aTags = self.browser.find_elements(By.TAG_NAME, "a")
            #print(len(aTags))
            #for tag in aTags: 
            #    if tag.get_attribute("data-hveid") == "CAIQw": 
            #        print(tag.get_attribute("href"))
            #        print("found")
                    
            tag = self.browser.find_element(By.XPATH, "//div[@class='hdtb-mitem'][1]/a[1]")
            imagePageURL = tag.get_attribute("href")

            urls = self.getImagesFromGoogle(imagePageURL, 2, 5, item)
            print(f"FOUND {len(urls)} URLS") 
            os.mkdir("./dataset/" + item)
            
            for i, url in enumerate(urls): 
                self.downloadImage(url, item, str(i) + ".jpg")
