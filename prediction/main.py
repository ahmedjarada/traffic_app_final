import os
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
from prediction.convert_to_image import convert
base_dir = Path(__file__).resolve().parent

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_app_final.settings')
django.setup()
images = os.listdir('images')

from records.models import *


for image in images:
    im = cv2.imread(f'{base_dir}\images\{image}')
    bbox, label, conf = cv.detect_common_objects(im)
    prediction = int(label.count('car') + label.count('bus') + label.count('truck'))
    new_record = Record.objects.create(prediction=prediction,
                                       street_reference=Street.objects.get(title='Al-Nasser St.'))





#
# print(bbox)
# print(label)
# print(conf)
# new_street = Street.objects.create(long=34.45602958878094, lat=31.531241864152936, title='Al-Nasser St.').save()

# output_image = draw_bbox(im, bbox, label, conf)
# plt.imshow(output_image)
# plt.show()
