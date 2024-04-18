def exact_color(input_image, resize, tolerance, zoom):
    # リサイズを実施
    img = Image.open(input_image)
    output_width = resize
    if img.size[0] > resize:
        width_per_c = (output_width / float(img.size[0]))
        hsize = int((float(img.size[1]) * width_per_c))
        img = img.resize((output_width, hsize), Image.ANTIALIAS)
    
    # 画像を一時ファイルとして保存
    resize_name = 'resize_' + input_image.split('/')[-1]  # ファイル名のみ抽出
    img.save(resize_name)

    # 色を抽出
    colors_x = extcolors.extract_from_path(resize_name, tolerance=tolerance, limit=5)
    colors_pre_list = [str(tup[0]) for tup in colors_x[0]]
    df_percent = [tup[1] for tup in colors_x[0]]
    df_color_up = [rgb2hex(*rgb) for rgb in colors_pre_list]
    df_color = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])

    # 描画
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.pie(df_color['occurence'], labels=df_color['c_code'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # カラーパレット
    for i, color in enumerate(df_color['c_code']):
        ax2.add_patch(patches.Rectangle((0, i), 1, 1, color=color))
        ax2.text(1.1, i + 0.5, color, verticalalignment='center', fontsize=12)

    ax2.set_xlim(0, 2)
    ax2.set_ylim(0, len(df_color['c_code']))
    ax2.axis('off')  # 軸を非表示にする

    # プロットの表示と画像の保存
    plt.show()
    fig.savefig('color_palette_and_pie_chart.png')

    # 一時ファイルの後始末
    os.remove(resize_name)  # 生成されたリサイズ画像を削除

# 使用例
exact_color("image/mike.jpg", resize=1000, tolerance=10, zoom=2)
