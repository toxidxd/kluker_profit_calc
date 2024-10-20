import os
import logging

from PIL import Image
import easyocr
from torch.autograd.profiler import profile

from opencv_module import get_borders

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def get_border(img):
#     for y in range(img.height):
#         # print(y, img.getpixel((50, y)))
#         pixel_color = img.getpixel((50, y))
#         red, green, blue = img.getpixel((50, y))[0:3]
#         if red in range(105, 130) and green in range(55, 70) and blue in range(203, 223):
#             # if pixel_color == (112, 80, 178):
#             result = (37, y, 559, y + 99)
#             return result


def crop_image(img, borders, num):
    logger.info(f"Cropping {num} image")
    img = Image.open(img)
    parsed_images = []
    img_crop = img.crop(borders)
    img_name = "crop_" + str(num) + ".jpg"
    img_crop.save(img_name)
    cropped_image = Image.open(img_name)
    name = " ".join(crop_name(cropped_image))
    per_hour = " ".join(crop_per_hour(cropped_image))
    price = " ".join(crop_price(cropped_image))
    parsed_image = [name, per_hour, price]

    return parsed_image


def crop_name(img):
    logger.info("Cropping name")
    img.crop((150, 0, 370, 65)).save("temp_name.png")
    return text_recognition("temp_name.png")


def crop_per_hour(img):
    logger.info("Cropping per hour")
    img.crop((400, 0, 560, 40)).save("temp_per_hour.png")
    return text_recognition("temp_per_hour.png")


def crop_price(img):
    logger.info("Cropping price")
    img.crop((415, 40, 556, 90)).save("temp_price.png")
    return text_recognition("temp_price.png")


def text_recognition(img_path):
    logger.info(f"Recognizing {img_path}")
    # reader = easyocr.Reader(["ru", "en"], gpu=True)
    reader = easyocr.Reader(["ru", "en"], gpu=False)
    result = reader.readtext(img_path, detail=0)

    return result


def calc_profit(data):
    profit_items = {}
    for item in data:
        print(item)
        if "," in item[1]:
            item[1] = item[1].replace(",", ".")

        if "+" in item[1]:
            item[1] = item[1].replace("+", "")

        if "З" in item[1]:
            item[1] = item[1].replace("З", "3")

        if 'k' in item[1]:
            item[1] = item[1].split("k")[0]
            if item[1].isalnum():
                hour = float(item[1]) * 1000
            else:
                hour = 1
        else:
            hour = float(item[1].split(" ")[0])

        # print(hour, end=" ")
        if "," in item[2]:
            item[2] = item[2].replace(",", ".")

        if " " in item[2]:
            item[2] = item[2].replace(" ", ".")

        price = float(item[2].split("k")[0]) * 1000

        # print(price)
        profit_items[item[0]] = price // hour
        # print(profit_items)
    return profit_items


def main():
    cropped_images = []
    crop_num = 0
    for template in os.listdir('templates'):
        logger.info(template)
        for img in os.listdir('screenshots'):
            logger.info(img)
            borders = get_borders(f'screenshots/{img}', f'templates/{template}')
            if borders != 0:
                logger.info(f"Found borders for {img}")
                cropped_images.append(crop_image(f'screenshots/{img}', borders, crop_num))
                crop_num += 1

    profit = {k: v for k, v in sorted(calc_profit(cropped_images).items(), key=lambda item: item[1])}
    for i, key in enumerate(profit.keys()):
        print(f'{i+1} {key}: {profit[key]}')


if __name__ == "__main__":
    main()
