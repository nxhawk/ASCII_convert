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
        inFILE.split(".")[0] + "_ASCII." + inFILE.split(".")[1]
    outTXT = folder + '\\' + inFILE.split(".")[0] + ".txt"
    print("Processing {}".format(inFILE))
    bg_code = (255, 255, 255)
    num_chars = len(char_list)

    image = cv2.imread(directory + "/" + inFILE, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape
    num_cols = 200
    num_rows = int(num_cols * width / height / 1.2)
    while True:
        cell_width = int(width / num_cols)
        cell_height = int(height / num_rows)
        if cell_height > 0 and cell_width > 0:
            break
        num_cols = num_cols - 1
        num_rows = int(num_cols * width / height / 1.2)
        if num_cols <= 0:
            cell_width = 6  # chieu rong 1 cell
            cell_height = 12  # chieu cao 1 cell
            num_cols = int(width / cell_width)
            num_rows = int(height / cell_height)
            break
    # lay size cua ki tu tuong trung cho ngon ngu render
    char_width, char_height = font.getsize(char_list[0])
    # size image output
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows
    # image output
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    allChar = []
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
                draw.text((j * char_width, i * char_height),
                          char, fill=partial_avg_color, font=font)
                f.write(char)
                allChar.append(partial_avg_color)
            f.write("\n")
        for R, G, B in allChar:
            f.write(str(R) + " " + str(G) + " " + str(B) + "\n")
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
