# it reads names from excel sheet and add it at paticular postion of image (certificate_template)
# it also takes signature as image and add it at paticular position of image (certificate_template)


import pytesseract
from PIL import Image,ImageDraw,ImageFont
import pandas as pd
import cv2
import numpy


# vist this link to download :  https://github.com/UB-Mannheim/tesseract/wiki
# and add path file 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


#returns tuple (x,y,w(width per character)) or false if text not found in image
def get_text_pos(img,text):

    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    box_length = len(d['level'])
    for i in range(box_length):
        if(d['text'][i] == text):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                print(x,y,w,h) # x,y ,width,height
                #returning x_pos  of middle text, y postion , pixel per character
                return (x+(w//2) ,y ,w//len(text))
    
    return False

#returns image after removing all text in text_list
# text_list : list of text to remove from image
def remove_text_from_image(img,text_list):
    #returns image after removing all text in text_list
    # text_list : list of text to remove from image

    # converting PIL image to cv2 image
    image = numpy.array(img) 
    # Convert RGB to BGR 
    image= image[:, :, ::-1].copy()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    inverted_thresh = 255 - thresh
    dilate = cv2.dilate(inverted_thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        ROI = thresh[y:y+h, x:x+w]
        data = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6').lower()
        print(data)
        if data.rstrip().lower() in text_list:
            image[y:y+h, x:x+w] = [255,255,255]


    # converting cv2 image to pil image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    #return image

    return image
                
#returns img after adding text in image at text_pos(x,y)
def add_text_in_image(img,text,text_pos):
    text_color = (0,0,0)
    img = img.convert('RGB')
    d= ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf",65)

    #calculating position where the name should start (half character of name is on left side and half on right side of center point)
    text_pos_x = text_pos[0]-(len(text)//2)*text_pos[2] #text_pos[2] holds pixel per character
    text_pos = (text_pos_x,text_pos[1])

    d.text(text_pos,text, fill=text_color,font=font)

    return img


#Adds signature image in main_img at signature_pos(x,y)
def add_signature_in_image(main_img,signature_img,signature_pos):

         

    copy_img = main_img.copy()
    copy_img.paste(signature_img,signature_pos)
    return copy_img



# reading name from excel sheet
data = pd.read_excel("certificates.xlsx")  #need to have this file and 'Name' column on it 
name_list = data['Name'].to_list()
name_list.append('Ram bahadur lamichhane')
name_list.append('Om B.K')


img = Image.open("main_cert.png")

    
text_pos = get_text_pos(img,"textiname")

signature_one_pos = get_text_pos(img,"img:one")[:2]
signature_two_pos = get_text_pos(img,"img:two")[:2] # it returns 3 tuple (x,y,w) w= width per character (not needed for image) so only taking first 2 tuple

img = remove_text_from_image(img,["textiname","img:one","img:two"])


for name in name_list:
    copy_img = img.copy()
    copy_img = add_text_in_image(img,name,text_pos)

    signature_img = Image.open("signature.png")

    copy_img = add_signature_in_image(copy_img,signature_img,signature_one_pos)
    copy_img = add_signature_in_image(copy_img,signature_img,signature_two_pos)
    
    copy_img.save("test_Cert_"+ name + ".png")