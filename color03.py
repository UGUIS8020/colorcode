import PIL
from PIL import Image
import cv2
import sklearn
from sklearn.cluster import KMeans


cv2_img = cv2.imread('image/mike.jpg')
cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
cv2_img.shape
(900, 1600, 3)
cv2_img = cv2_img.reshape(
    (cv2_img.shape[0] * cv2_img.shape[1], 3))
cv2_img.shape
(1440000, 3)

cluster = KMeans(n_clusters=5)
cluster.fit(X=cv2_img)

KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
    n_clusters=5, n_init=10, n_jobs=1, precompute_distances='auto',
    random_state=None, tol=0.0001, verbose=0)

cluster.cluster_centers_

cluster.cluster_centers_.shape
(5, 3)

format(255, '02x')
'ff'
'#%02x%02x%02x' % (255, 255, 255)
'#ffffff'
cluster_centers_arr = cluster.cluster_centers_.astype(
    int, copy=False)
from IPython.display import display
for rgb_arr in cluster_centers_arr:
    color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
    color_img = Image.new(
        mode='RGB', size=(32, 32), color=color_hex_str)
    display(color_img)

original_img = Image.open('./flower.jpg')
original_img.size
(1600, 900)
original_img.resize((320, 180))

# 幅と高さ64px × 横並び5画像 + 上下左右余白15pxずつの画像を作ります。
IMG_SIZE = 64
MARGIN = 15
width = IMG_SIZE * 5 + MARGIN * 2
height = IMG_SIZE + MARGIN * 2
print(width, height)

tiled_color_img = Image.new(
    mode='RGB', size=(width, height), color='#333333')

for i, rgb_arr in enumerate(cluster_centers_arr):
    color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
    color_img = Image.new(
        mode='RGB', size=(IMG_SIZE, IMG_SIZE),
        color=color_hex_str)
    tiled_color_img.paste(
        im=color_img,
        box=(MARGIN + IMG_SIZE * i, MARGIN))
tiled_color_img


