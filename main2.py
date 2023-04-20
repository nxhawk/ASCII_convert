import os
import numpy as np
import cv2
from PIL import Image, ImageDraw
from utils import char_list, font, FOLDER_RESULT
import threading

directory = os.getcwd() + "\image"
scale = 1


def main(inFILE):
    folder = FOLDER_RESULT + "\\" + inFILE.split(".")[0]
    # create folder result + name folder
    if not os.path.exists(folder):
        os.mkdir(folder)
    outFILE = folder + '\\' + \
        inFILE.split(".")[0] + "_ASCII_v2." + inFILE.split(".")[1]
    outTXT = folder + '\\' + inFILE.split(".")[0] + "_v2.txt"
    print("Processing {}".format(inFILE))
    bg_code = (255, 255, 255)
    num_chars = len(char_list)

    image = cv2.imread(directory + "/" + inFILE, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    num_cols = 200
    cell_width = width / num_cols
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    # lay size cua ki tu tuong trung cho ngon ngu render
    char_width, char_height = font.getsize(char_list[0])
    # size image output
    out_width = char_width * num_cols
    out_height = int(scale * char_height * num_rows)
    # image output
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    allChar = {}
    with open(outTXT, "w") as f:
        f.write(str(num_rows) + " " + str(num_cols) + "\n")
        for i in range(num_rows):
            for j in range(num_cols):
                # tach cell image [height, width, depth]
                partial_image = image[int(i*cell_height):min(int((i+1)*cell_height), height), int(
                    j*cell_width):min(int((j+1)*cell_width), width), :]
                partial_avg_color = np.sum(
                    np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
                partial_avg_color = tuple(
                    partial_avg_color.astype(np.int32).tolist())
                char = char_list[min(
                    int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
                if not (char in allChar.keys()):
                    allChar[char] = partial_avg_color
                else:
                    partial_avg_color = allChar[char]
                draw.text((j * char_width, i * char_height),
                          char, fill=partial_avg_color, font=font)
                f.write(char)
            f.write("\n")
        f.write(str(len(allChar))+"\n")
        for x, y in allChar.items():
            f.write(x)
            R, G, B = y
            f.write(" "+str(R) + " "+str(G)+" "+str(B)+"\n")
    out_image.save(outFILE)
    print("DONE process {}".format(inFILE))


if __name__ == '__main__':
    if not os.path.exists(FOLDER_RESULT):
        os.mkdir(FOLDER_RESULT)

    for file in os.listdir(directory):
        if os.path.isfile(directory+'/'+file):
            main(file)
            # thread = threading.Thread(target=main, args=(file,))
            # thread.start()
