import os
import logging
import sys

from PIL import Image
import easyocr

from opencv_module import get_borders

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


def crop_image(img, borders, num):
    logger.info(f"Cropping {num} image")
    img = Image.open(img)
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
    img.crop((252, 0, 724, 114)).save("temp_name.png")
    return text_recognition("temp_name.png")


def crop_per_hour(img):
    logger.info("Cropping per hour")
    img.crop((721, 0, 1024, 80)).save("temp_per_hour.png")
    return text_recognition("temp_per_hour.png")


def crop_price(img):
    logger.info("Cropping price")
    img.crop((776, 85, 1000, 162)).save("temp_price.png")
    return text_recognition("temp_price.png")


def text_recognition(img_path):
    logger.info(f"Recognizing {img_path}")
    # reader = easyocr.Reader(["ru", "en"], gpu=True)
    reader = easyocr.Reader(["ru", "en"], gpu=False)
    result = reader.readtext(img_path, text_threshold=0.9, detail=0)
    logger.info(f"Recognized: {result}")
    return result


def correct_profit_per_hour(data):
    logger.info(f"Correcting profit per hour")
    correct = []
    for ch in data:
        if ch == "." or ch.isdigit():
            correct.append(ch)
        else:
            correct.append('0')

    return float("".join(correct)) * 1000


def calc_profit(data):
    profit_items = {}
    for item in data:
        logger.info(item)
        if 'k' in item[1]:
            hour = item[1].split("k")[0].replace("+", "").replace(",", ".")
            hour = correct_profit_per_hour(hour)

        elif 'M' in item[1]:
            hour = item[1].split("M")[0].replace("+", "").replace(",", ".")
            hour = correct_profit_per_hour(hour)

        else:
            hour = float(item[1].split(" ")[0].replace("+", ""))

        if "," in item[2]:
            item[2] = item[2].replace(",", ".")

        if " " in item[2]:
            item[2] = item[2].replace(" ", ".")

        if "O" in item[2]:
            item[2] = item[2].replace("O", "0")

        if "k" in item[2]:
            price = float(item[2].split("k")[0]) * 1000
        elif "M" in item[2]:
            price = float(item[2].split("M")[0]) * 1000000
        elif "М" in item[2]: # russian M
            price = float(item[2].split("М")[0]) * 1000000
        else:
            price = float(item[2])

        logger.info(f"{item[0]} = {price} // {hour} = {price // hour}")
        profit_items[item[0]] = price // hour

    return profit_items

4.03
def main():
    cropped_images = []
    crop_num = 1
    for template in os.listdir('templates'):
        logger.info(f"Look template {template}")
        for img in os.listdir('screenshots'):
            logger.info(f"Seek in {img}")
            borders = get_borders(f'screenshots/{img}', f'templates/{template}')
            if borders != 0:
                logger.info(f"Found borders for {img}")
                cropped_images.append(crop_image(f'screenshots/{img}', borders, crop_num))
                crop_num += 1

    profit = {k: v for k, v in sorted(calc_profit(cropped_images).items(), key=lambda item: item[1])}
    for i, key in enumerate(profit.keys()):
        print(f'{i + 1} {key}: {profit[key]}')


if __name__ == "__main__":
    main()
