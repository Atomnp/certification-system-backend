# it reads names from excel sheet and add it at paticular postion of image (certificate_template)
# it also takes signature as image and add it at paticular position of image (certificate_template)


# import pandas as pd
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy
from utils.images import save_temporary_image, delete_temporary_image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid

TEXT_PREFIX = "xxtxtone"
IMAGE_PREFIX = "xximg"
PREFIXES = [TEXT_PREFIX, IMAGE_PREFIX]

# Might be useful for Windows User
# vist this link to download :  https://github.com/UB-Mannheim/tesseract/wiki
# and add path file

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"


def extract_placeholders(img: Image) -> dict:
    """Returns the placeholders present in the certificate template along with their position and lenth per character in pixels

    Args:
        img (Image):

    Returns:
        dict: keys contain the placeholder text and values (x,y,w) where x,y is the  midpoint of top
        left and top right and w is length per character of the placeholder text in pixels
    """

    #  Returns result containing box boundaries, confidences, and other information
    d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    box_length = len(d["level"])
    placeholders = {}
    for i in range(box_length):
        word = d["text"][i]
        if any([prefix in word for prefix in PREFIXES]):
            (x, y, w, h) = (d["left"][i], d["top"][i], d["width"][i], d["height"][i])
            placeholders[word] = (
                    x,
                    y,
                    w,
                    w // len(word),
                )
            
    return placeholders

def calculate_insert_position(text_pos,text,alignment="center"):
    (top_left_x, top_left_y,width, len_per_car) = text_pos

    mid_x = top_left_x + width//2

    if (alignment == "center"):
        # calculating position where name should start (half character of name is on left side and half on right side of center point)
        text_pos_x = mid_x - (len(text) * len_per_car) // 2

        return (text_pos_x,top_left_y)

    if alignment == "left":

        return (top_left_x,top_left_y)
        

def remove_text_from_image(pil_image, words_to_remove):
    """Removes the text from the image

    Args:
        pil_image (Image): Pillow image object
        words_to_remove (list(str)): list of words to remove

    Returns:
        Image: Image
    """
    words_to_remove = [word.lower() for word in words_to_remove]
    # convert image from pil to opencv format
    image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    inverted_thresh = 255 - thresh
    dilate = cv2.dilate(inverted_thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        ROI = thresh[y : y + h, x : x + w]
        data = pytesseract.image_to_string(ROI, lang="eng", config="--psm 6").lower()
        if data.rstrip().lower() in words_to_remove:
            image[y : y + h, x : x + w] = [255, 255, 255]

    # convert image from opencv to pil format
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def add_text_in_image(
    img,
    text,
    text_pos,
    font_size=100,
    text_color=(0, 0, 0),
    font="fonts/OpenSans-Regular.ttf",
):
    """Adds text to the image

    Args:
        img (Image): Template image
        text (string): Replacement text
        text_pos ((midx,midy,lpc)): Replacement position
        font_size (int, optional): font size. Defaults to 65.
        text_color (tuple, optional): color. Defaults to (0, 0, 0).
        font (str, optional): font type. Defaults to "arial.ttf".

    Returns:
        Image: image with text added
    """
    
    img = img.convert("RGB")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, font_size)

    
    
    d.text(text_pos, text, fill=text_color, font=font)

    return img


def add_signature_in_image(main_img, signature_img, signature_pos):
    """_summary_

    Args:
        main_img (Image):
        signature_img (Image):
        signature_pos (tuple): 2D coordinates of the signature

    Returns:
        Image: image
    """

    copy_img = main_img.copy()
    copy_img.paste(signature_img, signature_pos)
    return copy_img


# added another parameter 'placeholders'
def generate_certificate(image,person,map_dict,placeholders):
    """Takes templates,data and mapping  and generates certificate

    Args:
        template (_type_): Certificate template
        person(dict): object containing csv row to insert data into the certificate
        mappings (dict): csv column name to template placeholder mapping
        placeholders :

    Returns:
        ContentFile: This object is used to save the image in the database
    """
    
    for key,value in map_dict.items():
        text_pos = calculate_insert_position(placeholders[value['placeholder']],person[key],value['alignment'])
        image = add_text_in_image(image,person[key],text_pos)
    

    f = BytesIO()
    try:
        image.save(f, format="png")
        return ContentFile(f.getvalue(), name=uuid.uuid4().hex + ".png")
    finally:
        f.close()


    
    


         
        
        
            
    
    
    

if __name__ == "__main__":
    pass
    # img = Image.open("cert.png")
    # placeholders = extract_placeholders(img) 
    # img = remove_text_from_image(img, placeholders.keys())

    # name = "Rameshwor prashad lamichhane"

    # text_pos = calculate_insert_position(placeholders[TEXT_PREFIX],name,alignment="center")
    
    # img = add_text_in_image(img, "Rameshwor prashad lamichhane", text_pos)
    # img.save("temporary.png")

    # print(placeholders)

    # generate_test_certificate()
