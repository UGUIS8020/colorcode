import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import extcolors

from colormap import rgb2hex
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def exact_color(input_image, resize, tolerance, zoom):
    # リサイズを実施
    output_width = resize
    img = Image.open(input_image)
    if img.size[0] >= resize:
        width_per_c = (output_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(width_per_c)))
        img = img.resize((output_width, hsize), Image.ANTIALIAS)
        resize_name = 'resize_' + input_image
        img.save(resize_name)
    else:
        resize_name = input_image

    # 背景を設定する
    background = 'background.png'
    fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
    fig.set_facecolor('white')
    plt.savefig(background)
    plt.close(fig)

    # Dataframeの作成
    img_real = resize_name
    colors_x = extcolors.extract_from_path(img_real, tolerance=tolerance, limit=5)

    colors_pre_list = str(colors_x).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # RGBからHEXコードへの変換
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df_color = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])

    # 注釈を付ける
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(list_color, list_precent)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(160, 120), dpi=10)

    # donut plot
    wedges, text = ax1.pie(list_precent,
                           labels=text_c,
                           labeldistance=1.05,
                           colors=list_color,
                           textprops={'fontsize': 150, 'color': 'black'})
    plt.setp(wedges, width=0.3)

    # donut plotの中心に画像を追加
    img = mpimg.imread(resize_name)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (0, 0))
    ax1.add_artist(ab)

    # color palette
    x_posi, y_posi = 160, -170
    for c in list_color:
        y_posi += 180
        rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor=c)
        ax2.add_patch(rect)
        ax2.text(x=x_posi + 400, y=y_posi + 100, s=c, fontdict={'fontsize': 190})

    fig.set_facecolor('white')
    ax2.axis('off')
    bg = plt.imread('background.png')
    plt.imshow(bg)
    plt.tight_layout()
    fig.savefig('after_' + input_image)
    return plt.show()

# 使用例
# 使用例
exact_color("image/mike.jpg", resize=1000, tolerance=10, zoom=2)

