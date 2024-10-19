from PIL import Image
import easyocr


def get_border(img):
    for y in range(img.height):
        # print(y, img.getpixel((50, y)))
        pixel_color = img.getpixel((50, y))
        red, green, blue = img.getpixel((50, y))[0:3]
        if red in range(105, 130) and green in range(55, 70) and blue in range(203, 223):
            # if pixel_color == (112, 80, 178):
            result = (37, y, 559, y + 99)
            return result


def crop_image(img, borders):
    parsed_images = []

    for _ in range(6):
        print(_, end=" ")
        img_crop = img.crop(borders)
        img_name = "crop_" + str(_) + ".png"
        img_crop.save(img_name)
        cropped_image = Image.open(img_name)
        name = " ".join(crop_name(cropped_image))
        per_hour = " ".join(crop_per_hour(cropped_image))
        price = " ".join(crop_price(cropped_image))
        parsed_image = [name, per_hour, price]

        borders[1] += 121
        borders[3] += 121

        parsed_images.append(parsed_image)

    return parsed_images

def crop_name(img):
    img.crop((100,0,370,65)).save("temp_name.png")
    return text_recognition("temp_name.png")


def crop_per_hour(img):
    img.crop((370,0,520,40)).save("temp_per_hour.png")
    return text_recognition("temp_per_hour.png")


def crop_price(img):
    img.crop((383,40,520,90)).save("temp_price.png")
    return text_recognition("temp_price.png")


def text_recognition(img_path):
    reader = easyocr.Reader(["ru", "en"], gpu=True)
    # reader = easyocr.Reader(["ru", "en"], gpu=False)
    result = reader.readtext(img_path, detail=0)

    return result


def calc_profit(data):
    profit_items = {}
    for item in data:
        if ","  in item[1]:
            item[1] = item[1].replace(",", ".")

        if 'k' in item[1]:
            hour = float(item[1].split("k")[0]) * 1000
        else:
            hour = float(item[1].split(" ")[0])

        print(hour, end=" ")
        if ","  in item[2]:
            item[2] = item[2].replace(",", ".")
        price = float(item[2].split("k")[0]) * 1000

        print(price)
        profit_items[item[0]] = price // hour
        print(profit_items)
    return profit_items


def main():
    full_img = Image.open("img.png")
    # img = Image.open("img2.jpg")

    borders = list(get_border(full_img))
    print(borders)

    cropped_images = crop_image(full_img, borders)

    print(*cropped_images, sep="\n")

    profit = calc_profit(data=cropped_images)
    print(profit)


    # print(*recognized_data, sep="\n")
    #
    # calc_profit(recognized_data)


if __name__ == "__main__":
    main()
