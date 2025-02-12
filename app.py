import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import extcolors
import os
import glob

from colormap import rgb2hex
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def exact_color(input_image, resize, tolerance, zoom):
    try:
        print(f"\n処理開始: {input_image}")
        
        # 画像フォルダのパスを設定
        image_dir = os.path.join(os.getcwd(), 'image')
        output_dir = os.path.join(os.getcwd(), 'output')
        
        # 出力フォルダがなければ作成
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"出力フォルダを作成しました: {output_dir}")
        
        # 画像の完全パスを作成
        input_path = os.path.join(image_dir, input_image)
        print(f"入力画像パス: {input_path}")
        
        # リサイズを実施
        print("画像のリサイズを開始...")
        output_width = resize
        img = Image.open(input_path)
        print(f"元の画像サイズ: {img.size}")
        
        if img.size[0] >= resize:
            width_per_c = (output_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(width_per_c)))
            img = img.resize((output_width, hsize), Image.LANCZOS)
            resize_name = os.path.join(output_dir, 'resize_' + os.path.basename(input_image))
            img.save(resize_name)
            print(f"リサイズ後のサイズ: {img.size}")
        else:
            resize_name = input_path
            print("リサイズ不要")

        print("色情報の抽出を開始...")
        # Dataframeの作成
        img_real = resize_name
        colors_x = extcolors.extract_from_path(img_real, tolerance=tolerance, limit=10)
        print(f"抽出された色数: {len(str(colors_x).replace('([(', '').split(', (')[0:-1])}")

        colors_pre_list = str(colors_x).replace('([(', '').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

        # RGBからHEXコードへの変換
        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                              int(i.split(", ")[1]),
                              int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

        df_color = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])

        print("可視化の作成を開始...")
        # 注釈を付ける
        list_color = list(df_color['c_code'])
        list_precent = [int(i) for i in list(df_color['occurence'])]
        text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(list_color, list_precent)]
        
        # プロットの作成
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
        x_posi, y_posi, y_posi2 = 160, -170, -170
        for c in list_color:
            if list_color.index(c) <= 5:
                y_posi += 180
                rect = patches.Rectangle((x_posi, y_posi), 360, 160, facecolor=c)
                ax2.add_patch(rect)
                ax2.text(x=x_posi + 400, y=y_posi + 100, s=c, fontdict={'fontsize': 190})
            else:
                y_posi2 += 180
                rect = patches.Rectangle((x_posi + 1000, y_posi2), 360, 160, facecolor=c)
                ax2.add_artist(rect)
                ax2.text(x=x_posi + 1400, y=y_posi2 + 100, s=c, fontdict={'fontsize': 190})

        fig.set_facecolor('white')
        ax2.axis('off')
        plt.tight_layout()
        
        # 出力ファイルのパスを設定
        output_path = os.path.join(output_dir, 'analyzed_' + os.path.basename(input_image))
        fig.savefig(output_path)
        plt.close()
        print(f"分析結果を保存しました: {output_path}")
        
    except Exception as e:
        print(f"エラーが発生しました ({os.path.basename(input_image)}): {str(e)}")


if __name__ == "__main__":
    try:
        # 現在のディレクトリを表示
        print(f"現在のディレクトリ: {os.getcwd()}")
        
        # imageフォルダが存在しない場合は作成
        if not os.path.exists('image'):
            os.makedirs('image')
            print("imageフォルダを作成しました。画像ファイルを配置してください。")
            exit()
        
        # JPG画像を検索
        image_pattern = os.path.join('image', '*.jpg')
        image_files = glob.glob(image_pattern)
        
        # 画像が見つからない場合
        if not image_files:
            print("image フォルダ内にJPG画像が見つかりません。")
            exit()
        
        print(f"\n{len(image_files)}個の画像が見つかりました。分析を開始します...")
        print(f"見つかった画像: {[os.path.basename(f) for f in image_files]}")
        
        # 各画像を処理
        for image_path in image_files:
            image_name = os.path.basename(image_path)
            exact_color(
                input_image=image_name,
                resize=800,
                tolerance=32,
                zoom=1.0
            )
        
        print("\nすべての処理が完了しました。")
            
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")