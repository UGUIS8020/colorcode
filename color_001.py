import cv2
from sklearn.cluster import KMeans
from PIL import Image

# 画像を読み込む
cv2_img = cv2.imread('image/flower.jpg')
cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

# 画像データを1次元に変形
cv2_img = cv2_img.reshape((cv2_img.shape[0] * cv2_img.shape[1], 3))

# KMeans オブジェクトの生成
cluster = KMeans(n_clusters=5, random_state=0)

# クラスタリングの実行
cluster.fit(cv2_img)

# クラスターセンターを整数に変換
cluster_centers_arr = cluster.cluster_centers_.astype(int)

# 各クラスターセンターの色で画像を作成し、表示する
for rgb_arr in cluster_centers_arr:
    color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
    color_img = Image.new(mode='RGB', size=(32, 32), color=color_hex_str)
    color_img.show()

# 元の画像を処理
original_img = Image.open('image/flower.jpg')
original_img = original_img.resize((320, 180))

# タイル状の画像を作成
IMG_SIZE = 64
MARGIN = 15
width = IMG_SIZE * 5 + MARGIN * 2
height = IMG_SIZE + MARGIN * 2
print(width, height)

tiled_color_img = Image.new(mode='RGB', size=(width, height), color='#333333')

for i, rgb_arr in enumerate(cluster_centers_arr):
    color_hex_str = '#%02x%02x%02x' % tuple(rgb_arr)
    color_img = Image.new(mode='RGB', size=(IMG_SIZE, IMG_SIZE), color=color_hex_str)
    tiled_color_img.paste(im=color_img, box=(MARGIN + IMG_SIZE * i, MARGIN))

# タイル状の画像を表示
tiled_color_img.show()
