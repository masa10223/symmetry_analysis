from concurrent.futures import thread
import os,sys,re
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
from unittest.util import three_way_cmp
from PIL import Image, ImageTk
import cv2
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#### https://iatom.hatenablog.com/entry/2020/11/01/151945
#### を大いに参考にさせていただきました。


def scale_box(img, width, height):
    """
    指定した大きさに収まるように、アスペクト比を固定して、リサイズする。

    Args:
        img (_type_): _description_
        width (_type_): _description_
        height (_type_): _description_

    Returns:
        _type_: _description_
    """
    h, w = img.shape[:2]
    aspect = w / h
    if width / height >= aspect:
        nh = height
        nw = round(nh * aspect)
    else:
        nw = width
        nh = round(nw / aspect)

    dst = cv2.resize(img, dsize=(nw, nh))

    return dst

    """画像を重ねて合成する。

    Args:
        src (_type_): _description_
        overlay (_type_): _description_
        location (_type_): _description_

    Returns:
        _type_: _description_
    """
    _, _ = overlay.shape[:2]

    # 背景をPIL形式に変換
    src = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    pil_src = Image.fromarray(src)
    pil_src = pil_src.convert('RGBA')

    # オーバーレイをPIL形式に変換
    overlay = cv2.cvtColor(overlay, cv2.COLOR_BGRA2RGBA)
    pil_overlay = Image.fromarray(overlay)
    pil_overlay = pil_overlay.convert('RGBA')

    # 画像を合成
    pil_tmp = Image.new('RGBA', pil_src.size, (255, 255, 255, 0))
    pil_tmp.paste(pil_overlay, location, pil_overlay)
    result_image = Image.alpha_composite(pil_src, pil_tmp)

    # OpenCV形式に変換
    return cv2.cvtColor(np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

# Define a function to make the transparent rectangle

class embryo_gui():

    # 変数
    filepath = None
    threshold = None
    input_canvas = None
    output_canvas = None
    chg_out = None

    x_start,x_end = 0,0
    y_start,y_end = 0,0


    ##############
    #   初期設定  #
    ##############
    def __init__(self, main):
        ## 初期値設定##
        self.kernel_size = 8
        self.area_min = 4000
        self.area_max = 100000
        # ファイル削除処理
        self.file_del()
        # Clearボタン配置
        clear1 = Button(root, text=u'Undo', command=self.clear_clicked)
        clear1.grid(row=0, column=1)
        clear1.place(x=570, y=12)

        # 参照ボタン配置
        button1 = Button(root, text=u'Reference', command=self.button1_clicked)
        button1.grid(row=0, column=2)
        button1.place(x=640, y=12)

        # 閉じるボタン
        close1 = Button(root,text=u'Close',command=self.close_clicked)
        close1.grid(row=0,column=3)
        close1.place(x=740,y=12)

        # 参照ファイルパス表示ラベルの作成
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(root,textvariable=self.file1, width=60)
        self.file1_entry.grid(row=0, column=4)
        self.file1_entry.place(x=12,y=12)


    ##########################
    # ファイルを削除するメソッド #
    ##########################
    def file_del(self):
        if os.path.exists("./output_image_small.png") == True:
            os.remove("./output_image_small.png")
        if os.path.exists("./input_image.png") == True:
            os.remove("./input_image.png")

    ########################
    # フォームを閉じるメソッド #
    ########################
    def close_clicked(self):
        # メッセージ出力
        res = messagebox.askokcancel("確認", "Do you wish to close this form?")
        #　フォームを閉じない場合
        if res != True:
            # 処理終了
            return

        #不要ファイル削除
        self.file_del()
        #処理終了
        sys.exit()

    #################
    # 元に戻すメソッド #
    #################
    def clear_clicked(self):
        # メッセージ出力
        res = messagebox.askokcancel("確認", "Do you want to undo?")
        #　フォームを閉じない場合
        if res != True:
            # 処理終了
            return
        input_canvas.delete("draw-rectangle")


    ####################################
    # 参照ボタンクリック時に起動するメソッド #
    ####################################
    def button1_clicked(self):
        # ファイル種類のフィルタ指定とファイルパス取得と表示（.tifのみ)
        fTyp = [("画像ファイル","*.png"),("画像ファイル","*.tif")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        # 選択したファイルのパスを取得
        self.filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        # ファイル選択指定なし？
        if self.filepath == "":
            return
        # 選択したパス情報を設定
        self.file1.set(self.filepath)


        # 画像を保存を実施するボタンの生成と配置
        #self.button_save = Button(root,text=u"Save Image", command=self.save_clicked,width=10)
        #self.button_save.grid(row=0, column=0)
        #self.button_save.place(x=390, y=300)

        # ROIを設定するボタンの生成と配置
        self.button_draw = Button(root,text=u"Draw Area",command=self.draw_area,width=10)
        self.button_draw.grid(row=0, column=3)
        self.button_draw.place(x=390, y=270)


        # 画像ファイル読み込みと表示用画像サイズに変更と保存
        img = cv2.imread(self.filepath)
        img_resize = scale_box(img,320,240)
        #img_resize = cv2.resize(img,dsize=(320,240))
        cv2.imwrite("disp_img.png",img_resize)

        ## 拡大率 表示用の画面に合わせているのでずれるのを防止する。
        self.expand_ratio_y = img.shape[0]/240
        self.expand_ratio_x = img.shape[1]/320

        self.mask = np.ones((img.shape[0],img.shape[1]))

        # 入力画像を画面に表示
        self.disp_image = ImageTk.PhotoImage(file="disp_img.png")
        input_canvas.create_image(163, 122, image=self.disp_image)
        #input_canvas.create_text(163, 0, text="Original Image", fill="white", font=('Helvetica', '16', 'bold'))


        os.remove('disp_img.png')

    ########################################
    # マウスで操作しているときに起動するメソッド  #
    ########################################
    def draw_start(self, event):
        self.x_start, self.y_start = event.x, event.y
        # 最初の四角形を描画（見えないが、後でサイズを更新する）
        self.rect = input_canvas.create_rectangle(self.x_start, self.y_start, event.x, event.y, outline='blue', width=2, tag='draw-rectangle')

    def draw_smooth(self, event):
        self.x_end, self.y_end = event.x, event.y
        # 既存の四角形の座標を更新して、描画中の四角形を動的に表示（輪郭のみ）
        input_canvas.coords(self.rect, self.x_start, self.y_start, self.x_end, self.y_end)

    def draw_end(self, event):
        # マウスボタンを放した時の処理は特に変更しなくても、`draw_smooth`で更新した座標が適用されているため、追加の処理は不要です。
        pass
    #########################################
    # Draw Areaボタンクリック時に起動するメソッド #
    #########################################
    def draw_area(self):
        input_canvas.bind("<Button-1>", self.draw_start)
        input_canvas.bind("<B1-Motion>", self.draw_smooth)
        input_canvas.bind("<ButtonRelease-1>", self.draw_end)

        # 領域を切り取るボタンの生成と配置
        self.button_crop = Button(root,text=u"Crop Area",command=self.crop_area,width=10)
        self.button_crop.grid(row=0, column=3)
        self.button_crop.place(x=390, y=210)
    #########################################
    # Crop Areaボタンクリック時に起動するメソッド #
    #########################################
    def crop_area(self):
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath,0)
        ##拡大縮小の調整。
        print(self.y_start,self.y_end,self.x_start,self.x_end)
        self.y_start_exp = int(self.y_start * self.expand_ratio_y)
        self.x_start_exp = int(self.x_start * self.expand_ratio_x)
        self.y_end_exp = int(self.y_end * self.expand_ratio_y)
        self.x_end_exp = int(self.x_end * self.expand_ratio_x)
        ## 領域をとる
        img_cropped = img[self.y_start_exp:self.y_end_exp,self.x_start_exp:self.x_end_exp]
        print(img_cropped.shape)
        print(self.y_start_exp,self.y_end_exp,self.x_start_exp,self.x_end_exp)
        cv2.imwrite("output_image_crop.png",img_cropped)
        self.chg_out = img_cropped

        # 表示用に画像サイズを小さくする
        img2 = scale_box(img_cropped,320,240)
        #img2 = cv2.resize(img_cropped,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_crop_small.png",img2)
        # 画像をセット
        self.out_image_crop_disp = ImageTk.PhotoImage(file="output_image_crop_small.png")
        output_canvas.create_image(160, 120, image=self.out_image_crop_disp)
        #output_canvas.create_text(160, , text="Cropped Image", fill="white", font=('Helvetica', '16', 'bold'))

        ## 削除
        os.remove("output_image_crop_small.png")
        os.remove("output_image_crop.png")

        # 閾値のエントリーバーの設定
        self.thr_entry = Entry(root)
        self.thr_entry_label = Label(root,text = 'Type Threshold (0-255)')
        self.thr_entry_label.place(x=380,y=45)
        self.thr_entry.place(x=390, y = 70, width = 120)
        
        self.thr_scale = Scale(root,
                               command = self.detect_area_2,
                               orient =HORIZONTAL,
                               from_=0,
                               to=255,
                               resolution=1,
                               length = 120,
                               )
        self.thr_scale_label = Label(root,text = 'Scroll Threshold (0-255)')
        self.thr_scale_label.place(x=380,y=95)
        self.thr_scale.place(x =390, y = 120)
        
        # Scaleウィジェットをクリックしたときにフォーカスを設定
        self.thr_scale.bind("<Button-1>", lambda e: self.thr_scale.focus_set())

        # キーボードイベントをハンドリング
        self.thr_scale.bind("<Up>", self.increment_scale)
        self.thr_scale.bind("<Down>", self.decrement_scale)

        
        #input_canvas.create_window(390, 50, window=self.thr_entry)
        self.binarize = Button(root, text='Detect Area',command =self.detect_area,width=10)
        self.binarize.place(x=390, y=165)
        
        self.button_crop = Button(root,text=u"Binarize",command=self.binarize_,width=10)
        self.button_crop.place(x=540, y=350)
        
        
        self.thr_min_entry = Entry(root)
        self.thr_min_label = Label(root,text = 'Threshold min')
        self.thr_min_entry.place(x=750, y = 390, width = 100)
        self.thr_min_label.place(x=640, y = 390)
        
        self.thr_max_entry = Entry(root)
        self.thr_max_label = Label(root,text = 'Threshold max')
        self.thr_max_entry.place(x=750, y = 410, width = 100)
        self.thr_max_label.place(x=640, y = 410)
        
        self.calculate_progress = ttk.Progressbar(
            root,
            orient="horizontal",
            length = 300,
            mode="determinate",   #非確定的
        )
        #self.calculate_progress.pack()
        #now_data_label = Label(root,textvariable=self.now_dat)
        self.button_calculate = Button(root,text=u"Calculate",command=self.calculate,width=10)
        self.button_calculate.place(x=730, y=350)

        self.button_calculate = Button(root,text=u"Stop",command=self.stop_calculate,width=10)
        self.button_calculate.place(x=730, y=320)

    #############################################
    # Detect Area ボタンクリック時に起動するメソッド #
    ############################################

    def detect_area(self):
        try:
            thr = int(self.thr_entry.get())
        except:
            thr = int(self.thr_scale.get())
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # 切り取られた領域
        img_cropped = img[self.y_start_exp:self.y_end_exp,self.x_start_exp:self.x_end_exp]
        # 二値化する.
        i_out = self.threshold_correction(img_cropped, thr)
        # ゴミをとる. + なめす
        opening = self.remove_(i_out)
        # 輪郭を取ってくる。
        img_contour,_ = self.collect_regions(img_cropped, opening)
        # GUIに表示する用の画像ファイルを作成
        #img2 = cv2.addWeighted(self.img_bg,0.9,self.img_fg,0.1,0)
        cv2.imwrite("output_image_crop_overlay.png",img_contour)
        # 表示用に画像サイズを小さくする
        img_contour_resize = scale_box(img_contour,320,240)
        #img2 = cv2.resize(self.img_exp,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_crop_bin_small.png",img_contour_resize)
        self.out_image_rec = ImageTk.PhotoImage(file="output_image_crop_bin_small.png")
        output_canvas.create_image(160, 120, image=self.out_image_rec)

        os.remove("output_image_crop_bin_small.png")
        os.remove("output_image_crop_overlay.png")
        
    def detect_area_2(self,args):
        """_summary_
        scale barのために detect_area function
        """
        thr = int(self.thr_scale.get())
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # 切り取られた領域
        img_cropped = img[self.y_start_exp:self.y_end_exp,self.x_start_exp:self.x_end_exp]
        # 二値化する.
        i_out = self.threshold_correction(img_cropped, thr)
        # ゴミをとる. + なめす
        opening = self.remove_(i_out)
        # 輪郭を取ってくる。
        img_contour,_ = self.collect_regions(img_cropped, opening)
        # GUIに表示する用の画像ファイルを作成
        #img2 = cv2.addWeighted(self.img_bg,0.9,self.img_fg,0.1,0)
        cv2.imwrite("output_image_crop_overlay.png",img_contour)
        # 表示用に画像サイズを小さくする
        img_contour_resize = scale_box(img_contour,320,240)
        #img2 = cv2.resize(self.img_exp,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_image_crop_bin_small.png",img_contour_resize)
        self.out_image_rec = ImageTk.PhotoImage(file="output_image_crop_bin_small.png")
        output_canvas.create_image(160, 120, image=self.out_image_rec)

        os.remove("output_image_crop_bin_small.png")
        os.remove("output_image_crop_overlay.png")


    def remove_(self, img):
        kernel = np.ones((self.kernel_size,self.kernel_size), np.uint8)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        return opening

    def collect_regions(self,img, opening):
        # 抽出領域をたくさんとる。
        contours_new,_ = cv2.findContours(opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0, len(contours_new)):
            if len(contours_new[i]) > 0:
            # remove small objects
                if (cv2.contourArea(contours_new[i]) > self.area_min )& (cv2.contourArea(contours_new[i]) < self.area_max ) :
                    continue
                cv2.polylines(img, contours_new[i], True, (0, 255, 255), 5)
                rect = contours_new[i]
                x, y, w, h = cv2.boundingRect(rect)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            else:
                messagebox.showerror('ERROR!!', 'No area to extract!!')
                input_canvas.delete("draw-rectangle")

        return img, contours_new
    
    def increment_scale(self, event):
        value = self.thr_scale.get()
        if value < 255:  # 最大値を超えないように
            self.thr_scale.set(value + 1)

    def decrement_scale(self, event):
        value = self.thr_scale.get()
        if value > 0:  # 最小値を下回らないように
            self.thr_scale.set(value - 1)

    #########################################
    # Binarize ボタンクリック時に起動するメソッド #
    #########################################
    def binarize_(self):
        try:
            thr = int(self.thr_entry.get())
        except:
            thr = int(self.thr_scale.get())
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # 切り取られた領域
        img_cropped = img[self.y_start_exp:self.y_end_exp,self.x_start_exp:self.x_end_exp]
        # 二値化する.
        i_out = self.threshold_correction(img_cropped, thr)
        # ゴミをとる. + なめす
        opening = self.remove_(i_out)
        # 輪郭を取ってくる。
        _,contours_new = self.collect_regions(img_cropped, opening)
        # 最大領域の内側に入っているのものを全て塗りつぶす
        contours_new_max = max(contours_new, key=lambda x: cv2.contourArea(x))
        img_binarize = cv2.drawContours(img_cropped, [contours_new_max], 0, (0,0,0), -1)
        img_binarize_rescale = scale_box(img_binarize,320,240)
        cv2.imwrite("output_image_crop_bin.png",img_binarize_rescale)
        self.img_binarize_rescale = ImageTk.PhotoImage(file="output_image_crop_bin.png")
        output_canvas.create_image(160, 120, image=self.img_binarize_rescale)
        
        os.remove("output_image_crop_bin.png")


    ##########################################
    # Calculate ボタンクリック時に起動するメソッド #
    ##########################################
    def calculate(self):
        thr_min = int(self.thr_min_entry.get())
        thr_max = int(self.thr_max_entry.get())
        filename_ = os.path.splitext(os.path.basename(self.filepath))[0]
        gene = re.findall(r'[A-Za-z0-9]+',filename_)[0]
        os.makedirs('./output_fig/{}/{}'.format(gene,filename_),exist_ok=True)
        os.makedirs('./output_csv/{}'.format(gene),exist_ok=True)
        result_df = pd.DataFrame()
        if thr_min >= thr_max:
            messagebox.showerror('エラー', 'Threshold Max is less than Threshold Min')
        for THRESHOLD in range(thr_min,thr_max+1):
            self.calculate_progress['value'] = int((THRESHOLD /(thr_max-thr_min))*100) 
            for angle in range(-5,6):
                img_exp = self.make_fig_exp_area(THRESHOLD)
                plt.imsave('./output_fig/{}/{}/{}.png'.format(gene,filename_,filename_+'_{}'.format(THRESHOLD)+'_{}'.format(angle)),img_exp)
                try:
                    shape_ = (img_exp.shape)
                    img_exp = self.padding_img(img_exp)
                    img_exp_rot = self.rotate_binary_img(img_exp, angle)
                    Left, Right = self.split_crop_area(img_exp_rot)
                    union, intersection, _, _ = self.iou(Left,Right)
                    assym = 1 - intersection/union
                    result = []
                    result.append([gene,filename_,THRESHOLD,angle,assym,self.y_start_exp,self.y_end_exp,self.x_start_exp,self.x_end_exp])
                    result = np.array(result)
                    result_df_tmp = pd.DataFrame(result)
                    result_df_tmp.columns = ['gene','filename','threshold','angle','assymetric_value','y_start','y_end','x_start','x_end']
                    result_df = result_df.append(result_df_tmp)
                    result_df.to_csv('./output_csv/{}/{}.csv'.format(gene,filename_),index=False)
                    root.update_idletasks()
                except:
                    pass

    def stop_calculate(self):
        value = self.calculate_progress['value']
        self.calculate_progress.stop()
        self.calculate_progress['value'] = value

    def make_fig_exp_area(self,threshold):
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # 切り取られた領域
        img_cropped = img[self.y_start_exp:self.y_end_exp,self.x_start_exp:self.x_end_exp]
        # 二値化する.
        i_out = self.threshold_correction(img_cropped, threshold)
        # ゴミをとる. + なめす
        opening = self.remove_(i_out)
        # 輪郭を取ってくる。
        _,contours_new = self.collect_regions(img_cropped, opening)
        # 最大領域の内側に入っているのものを全て塗りつぶす
        contours_max = max(contours_new, key=lambda x: cv2.contourArea(x))
        # ピッタリの画像を作成。
        x, y, w, h = cv2.boundingRect(contours_max)
        mask = np.ones((h,w))
        contours_max[:,0][:,0] =contours_max[:,0][:,0] -x
        contours_max[:,0][:,1] = contours_max[:,0][:,1] -y
        # 配列を作成。
        img_exp = cv2.drawContours(mask, [contours_max], 0, (0,0,0), -1)
        return 1-img_exp

    def split_crop_area(self,binary):
        """_summary_

        Args:
            binary (_type_): _description_

        Returns:
            _type_: _description_
        """
        #ret, binary = cv2.threshold(img_exp, thr, 1, cv2.THRESH_BINARY_INV)
        ## 左右の領域に分割する。
        Left = binary[:,:int(binary.shape[1]/2)]
        Right = np.fliplr(binary[:,int(binary.shape[1]/2):])
        return Left, Right

    def iou(self,a,b):
        """_summary_

        Args:
            a (_type_): _description_
            b (_type_): _description_

        Returns:
            _type_: _description_
        """
        union = 0
        intersection = 0
        union_coord = np.zeros([a.shape[0],a.shape[1]])
        intersection_coord =  np.zeros([a.shape[0],a.shape[1]])
        if (a.shape[0] == b.shape[0]) and (a.shape[1] == b.shape[1]):
            for i in range(a.shape[0]):
                for j in range(a.shape[1]):
                    if (a[i,j] == 1) and  (b[i,j] == 1):
                        intersection += 1
                        union += 1
                        union_coord[i,j] = 1
                        intersection_coord[i,j] = 1
                    elif ((a[i,j] == 0) and  (b[i,j] == 1)) or ((a[i,j] == 1) and  (b[i,j] == 0)):
                        union += 1
                        union_coord[i,j] = 1
                    else:
                        continue

        return union, intersection, union_coord, intersection_coord

    def rotate_binary_img(self,img_exp_pre, angle = 0):
        """_summary_

        Args:
            img_exp_pre (_type_): _description_
            angle (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        mu = cv2.moments(img_exp_pre, False)
        gx,gy= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
        #高さを定義
        height = img_exp_pre.shape[0]
        #幅を定義
        width = img_exp_pre.shape[1]

        #スケールを指定
        scale = 1.0
        #getRotationMatrix2D関数を使用
        trans = cv2.getRotationMatrix2D((gx,gy), angle , scale)
        #アフィン変換
        img_exp_rotate = cv2.warpAffine(img_exp_pre, trans, (width,height))

        return img_exp_rotate

    def padding_img(self,img_exp_rotate):
        """_summary_

        Args:
            img_exp_rotate (_type_): _description_

        Returns:
            _type_: _description_
        """
        if img_exp_rotate.shape[1] % 2 == 1:
            ## 横の長さが偶数になるように調整。
            img_exp_rotate = np.pad(img_exp_rotate,((0,0,),(0,1)))
        return img_exp_rotate


    ##################################
    # 画像保存ボタンクリック時のメソッド #
    ##################################
    def save_clicked(self):
        # 保存用のdirの作成
        os.makedirs('./output_fig',exist_ok=True)
        os.makedirs('./output_csv',exist_ok=True)
        # ファイル保存のダイアログ出力
        res = messagebox.askokcancel("確認", "Do you save as .png with the same filename?")
        #　フォームを閉じない場合
        if res != True:
            # 処理終了
            return
        # ファイル名を取得
        filename = os.path.basename(self.filepath)
        img_save_path = './output_fig/'+str(filename)+'.png'
        data_save_path = './output_csv/'+str(filename)+'.csv'

        cv2.imwrite(img_save_path,self.img_exp)
        df_coord = pd.DataFrame(np.array(self.crop_coord).reshape(-1,8))
        df_coord.columns = ['x_start','x_end','y_start','y_end','x_','y_','w_','h_']
        df_coord.insert(0,'filename',filename)
        df_coord.to_csv(data_save_path,index=False)



    ########################
    # 二値化するときのメソッド #
    ########################
    def threshold_correction(self, image, threshold):
        img_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        img_HSV = cv2.GaussianBlur(img_HSV, (5, 5), 3)
        img_H, img_S, img_V = cv2.split(img_HSV)
        _, binary = cv2.threshold(img_H, threshold, 255, cv2.THRESH_BINARY)
        return binary

    def threshold_correction_inv(self, image, threshold):
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_OTSU)
        return binary



if __name__ == '__main__':
    # 画面のインスタンス生成
    root = Tk()
    root.title("Embryo Expression Region Detecter")
    # GUI全体のフレームサイズ
    root.geometry("900x450")
    # 出力ファイル画像表示の場所指定とサイズ指定
    output_canvas = Canvas(root, width=320, height=240)
    output_canvas.place(x=540, y=90)
    #output_canvas.create_text(685, 10, text="Cropped Image", fill="white", font=('Helvetica', '16', 'bold'))

    # 入力ファイル画像表示の場所指定とサイズ指定
    input_canvas = Canvas(root, width=320, height=240)
    input_canvas.place(x=5, y=90)
    #input_canvas.create_text(150, 10, text="Original Image", fill="white", font=('Helvetica', '16', 'bold'))
    # GUI表示
    embryo_gui(root)
    root.mainloop()