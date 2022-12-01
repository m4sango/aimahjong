import cv2
# import matplotlib.pyplot as plt
# import numpy as np
# import tensorflow as tf
from PIL import ImageGrab
from roboflow import Roboflow

from image_util import pil2cv

CLASS_NAMES = ['1m', '1p', '1s', '2m', '2p', '2s', '3m', '3p', '3s', '4m', '4p', '4s', '5m', '5p', '5s', '6m', '6p',
               '6s', '7m', '7p', '7s', '8m', '8p', '8s', '9m', '9p', '9s', 'ch', 'hk', 'ht', 'na', 'pe', 'sy', 'to']
IMG_HEIGHT = 160
IMG_WIDTH = 160


def get_cv_img():
    img = ImageGrab.grab()
    return pil2cv(img)


def show_img(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def load_model():
#     return tf.keras.models.load_model('/Users/muramatsusho/IdeaProjects/aimahjong/model/transfer_4')


# def sort_pai(l: list):
#     for i, e in enumerate(l):
#         if

def detect():
    img = get_cv_img()
    img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    # img_bgr = cv2.resize(img_bgr, dsize=None, fx=0.5, fy=0.5)
    height, width = img_bgr.shape[:2]
    tehai_img = img_bgr[int(0.8 * height):height, 0:width]
    cv2.imwrite("temp.png", tehai_img)

    rf = Roboflow(api_key="rWvZap4o8irdpvDwDW1D")
    project = rf.workspace().project("aimahjong")
    model = project.version(1).model

    result = model.predict("temp.png", confidence=50, overlap=50).json()
    result = sorted([x["class"] for x in result["predictions"]])
    # infer on a local image
    print(f"tehai size = {len(result)}")
    print(result)

    # img_gray = cv2.cvtColor(tehai_img, cv2.COLOR_BGR2GRAY)
    # ret, img_bin = cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours = list(filter(lambda x: cv2.contourArea(x) > 1000, contours))
    #
    # result_img_l = []
    # for c in contours:
    #     x, y, w, h = cv2.boundingRect(c)
    #     result_img_l.append(tehai_img[y:y + h, x:x + w])
    #
    # fig = plt.figure(figsize=(24, 6))
    # for index, img in enumerate(result_img_l):
    #     # show_img(img)
    #     ax = fig.add_subplot(1, len(result_img_l), index + 1)
    #     ax.title.set_text(index)
    #     ax.imshow(img, 'gray')
    #     ax.axis('off')
    #
    # plt.show()
    #
    # # model = load_model()
    # # model.summary()
    # #
    # tehai_l = []
    # for img in result_img_l:
    #     tf_img = tf.convert_to_tensor(img, dtype=tf.float32)
    #     tf_img = tf.expand_dims(tf_img, 0)
    #     tf_img = tf.image.resize(tf_img, [IMG_HEIGHT, IMG_WIDTH])
    #
    #     predictions = model.predict(tf_img)
    #     score = tf.nn.softmax(predictions[0])
    #     print(
    #         "This image most likely belongs to {} with a {:.2f} percent confidence.".format(
    #             CLASS_NAMES[np.argmax(score)], 100 * np.max(score))
    #     )
    #     tehai_l.append(CLASS_NAMES[np.argmax(score)])
    #
    # print(tehai_l)


if __name__ == '__main__':
    detect()
