import cv2
import numpy as np
from skimage import exposure

def match_histograms(source, reference):
    """ヒストグラムマッチングを行い、色をオリジナルに近づける"""
    matched = exposure.match_histograms(source, reference, multichannel=True)
    return matched

# 画像を読み込む
source_img = cv2.imread("camera2.jpg")  # 補正したい画像
reference_img = cv2.imread("original.jpg")  # 基準となるオリジナル画像

# BGR → RGB に変換
source_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB)
reference_img = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)

# ヒストグラムマッチング
matched_img = match_histograms(source_img, reference_img)

# RGB → BGR に戻して保存
matched_img = cv2.cvtColor((matched_img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
cv2.imwrite("matched.jpg", matched_img)