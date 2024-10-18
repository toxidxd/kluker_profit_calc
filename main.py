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


def text_recognition(img_path):
    reader = easyocr.Reader(["ru", "en"], gpu=True)
    result = reader.readtext(img_path, detail=0)

    return result


def calc_profit(data):
    for item in data:
        for i in item:
            if "в час" in i:
                if "." or "," in i:
                    # print(i)
                    hour = float(i.split(".")[0]) * 1000
                    print('1', hour)
                else:
                    hour = float(i.split(" ")[0])
                    print('2', hour)

        for i in item:
            if ("." or "," in i) and "в час" not in i:
                print('3', i)


def main():
    img = Image.open("image.png")
    # img = Image.open("img2.jpg")
    borders = list(get_border(img))
    print(borders)
    im_crop = img.crop(borders)

    # im_crop.show()
    print(img.height // (borders[3] - borders[1]))
    # im_crop.save("crop.png")

    recognized_data = []
    for _ in range(6):
        print(_)
        im_crop = img.crop(borders)
        im_crop.save("crop_" + str(_) + ".png")
        recognized_data.append(text_recognition("crop_" + str(_) + ".png"))
        borders[1] += 121
        borders[3] += 121

    print(*recognized_data, sep="\n")

    calc_profit(recognized_data)


if __name__ == "__main__":
    main()
