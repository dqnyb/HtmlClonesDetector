import os
import re
import numpy as np
from difflib import SequenceMatcher
from os import listdir
from PIL import Image
import imagehash

from os.path import isfile, join
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage import metrics
from html_similarity import style_similarity, structural_similarity, similarity
from deep_translator import GoogleTranslator
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from scipy.spatial.distance import cosine


## ration = 2M/T
## M - numarul de caractere care se potrivesc exact
# T - suma lungimilor celor 2 text
# Gestalt pattern matching algorithm
# Ideea : Comparam doua secvente in paralel si o gasim pe cea mai lunga subsecv comuna si apelam recursiv pe celelalte ramase - algoritmul este deja implementat in difflib !

def calculate_ssim(imageA, imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(grayA, grayB, full=True)
    return score


def calculate_feature_similarity(image_path1, image_path2):
    base_model = VGG16(weights='imagenet', include_top=False)
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)

    def preprocess_image(image_path):
        img = image.load_img(image_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        return img_data

    img1 = preprocess_image(image_path1)
    img2 = preprocess_image(image_path2)

    features_img1 = model.predict(img1)
    features_img2 = model.predict(img2)

    features_img1 = features_img1.flatten()
    features_img2 = features_img2.flatten()
    similarity = 1 - cosine(features_img1, features_img2)

    return similarity

def compare_images_ssim(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)


    image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]), interpolation=cv2.INTER_AREA)

    b1, g1, r1 = cv2.split(image1)
    b2, g2, r2 = cv2.split(image2)

    ssim_b = ssim(b1, b2, data_range=b1.max() - b1.min())
    ssim_g = ssim(g1, g2, data_range=g1.max() - g1.min())
    ssim_r = ssim(r1, r2, data_range=r1.max() - r1.min())

    final_ssim = np.mean([ssim_r, ssim_g, ssim_b])

    # print(f"📊 SSIM Final: {final_ssim:.2f}")

    return final_ssim





def take_screenshot(html_file, output_file):
    html_path = os.path.abspath(html_file)
    file_url = f"file://{html_path}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(file_url)

    driver.save_screenshot(output_file)
    driver.quit()
    print(f"Screenshot saved as {output_file}")


# take_screenshot("tier2/healthfly.in.html", "example.png")
# take_screenshot("tier2/mariner-energy.com.html", "example1.png")


# score = compare_images_ssim("example.png", "example1.png")

# score = compare_images_ssim("example.png", "example1.png")
# print(f"SSIM Similarity Score: {score:.2f}")

def similarity_html(file1, file2):
    file1 = os.path.expanduser(file1)
    file2 = os.path.expanduser(file2)

    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        content1 = f1.read()
        content2 = f2.read()

    k = 0.3
    return k * structural_similarity(content1, content2) + (1 - k) * style_similarity(content1, content2)

# score = similarity_html("~/Desktop/Veridion/tier1/aemails.org.html",
#                         "~/Desktop/Veridion/tier1/akashinime.guru.html")

# print(f"Similarity score: {score:.2%}")




def add_from_tier(file3):
    return [f for f in listdir(file3) if isfile(join(file3, f)) and f != ".DS_Store"]






def create_images(onlyfiles,number):
    for i in onlyfiles:
        output_path = os.path.join("images/", f"{i}.png")
        take_screenshot(os.path.join(f"tier{number}", i), output_path)


final_list = [];
def check_all(onlyfiles,number):
    remaining_files = onlyfiles[:]
    final_list = []
    # create_images(onlyfiles)
    while remaining_files:
        i = remaining_files.pop(0)
        group = [i]
        for m in remaining_files[:]:
            # print(i)
            # print(m)
            score = similarity_html(f"tier{number}/{i}", f"tier{number}/{m}")
            # print()
            score_image = compare_images_ssim(f"images/{i}.png", f"images/{m}.png")
            feature_similarity = calculate_feature_similarity(f"images/{i}.png", f"images/{m}.png")
            # print(score)
            # print(score_image)
            print(f"Feature-based similarity (Cosine similarity): {feature_similarity}")
            if (score > 0.8 and feature_similarity > 0.6) or (score > 0.3 and score_image > 0.9 and feature_similarity > 0.6):
                group.append(m)
                remaining_files.remove(m)
            elif (feature_similarity > 0.75):
                group.append(m)
                remaining_files.remove(m)

        final_list.append(group)
    return final_list


# create_images(onlyfiles)
#
# file3 = "tier4"
# onlyfiles = add_from_tier(file3)
# create_images(onlyfiles,4)
# final_list = check_all(onlyfiles,4)
# print(final_list)



for i in range(1,5):
    print(f"Working on file{i} : ")
    file3 = f"tier{i}"
    onlyfiles = add_from_tier(file3)
    print(f"original list : {onlyfiles}")
    create_images(onlyfiles,i)
    final_list = check_all(onlyfiles,i)
    print(f"file{i} : {final_list}")



# image_dir = "images/"
# if os.path.exists(image_dir):
#     for file in os.listdir(image_dir):
#         file_path = os.path.join(image_dir, file)
#         if os.path.isfile(file_path):
#             os.remove(file_path)



# 'amt-avaluos.online.html', 'amcun3.online.html'

#
score = similarity_html(f"tier4/1-win-cazinos-club.org.ru.html", f"tier4/mirror-wulkan-russia.org.ru.html")
print(score)
# # # #
score = compare_images_ssim("images/1-win-cazinos-club.org.ru.html.png", "images/mirror-wulkan-russia.org.ru.html.png")
print(f"SSIM Similarity Score: {score}")

feature_similarity = calculate_feature_similarity("images/1win-official-site-casinoz.org.ru.html.png", "images/mirror-wulkan-russia.org.ru.html.png")
print(f"Feature-based similarity (Cosine similarity): {feature_similarity}")

imageA = cv2.imread("images/1-win-cazinos-club.org.ru.html.png")
imageB = cv2.imread("images/mirror-wulkan-russia.org.ru.html.png")

scor = calculate_ssim(imageA,imageB)
print(scor)

