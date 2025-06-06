class MyOs:

    def multi_thread(self, obj, data, num, flag=False):
        """
        并发的封装
        :param obj: 并发执行的函数
        :param data: 并非需要的数据
        :param num: 并发数
        :param flag: 用于执行obj函数传两个参数使用，默认一个参数
        :return: 执行
        """
        threads_list = []
        # flag :True 允许传两个参数
        if flag:
            for value in data:
                threads_list.append(threading.Thread(target=obj, args=(value, flag), name=f"进程{int(time.time())}"))
        else:
            for value in data:
                threads_list.append(threading.Thread(target=obj, args=(value,), name=f"进程{int(time.time())}"))
        # 开始线程计数
        num_one = 0
        # 结束线程计数
        num_two = 0
        # 每次执行的并发数
        num = int(num)
        # 开始线程计数，小于数据条数，就启动线程处理数据
        while num_one < len(data):
            # 每次启动线程的并发数
            for i in range(num):
                print("{}{}".format(threading.current_thread().name, num_one))
                threads_list[num_one].start()
                num_one += 1
                # 开始线程计数，大于数据条数，跳出循环
                if num_one >= len(data):
                    break
            # 每次等待线程的并发数结束
            for i in range(num):
                threads_list[num_two].join()
                num_two += 1
                # 开始线程计数，大于数据条数，跳出循环
                if num_two >= len(data):
                    break

    def filelist(self, file_dir):
        """
        查找文件夹下的所有文件，包含子目录、孙子目录下所有的文件
        :param file_dir: 文件夹路径
        :return: 返回文件列表
        """
        if os.path.exists(file_dir) == False:
            # 判断文件路径是否存在，不存在直接返回
            return "{}文件路径".format(file_dir)
        # 拉出根目录下的所有文件
        path_list = []
        for root, dirs, files in os.walk(file_dir):
            # root 根目录
            # dirs 子目录
            # files 子目录文件
            # 主要拉出根路径的文件
            if root == file_dir and dirs != []:
                # print(root)
                for i in range(len(files)):
                    paths = os.path.join(root, files[i])
                    path_list.append(paths)
                    # print(paths)
                # print("\n")
            # 主要拉出根目录下的所有子目录的文件
            if dirs == []:
                # print('目录路径    ：',root)
                # print('子目录名称  ：',dirs)
                # print('目录下的文件：',files)
                # print("\n")
                # print(root)
                for i in range(len(files)):
                    paths = os.path.join(root, files[i])
                    path_list.append(paths)
                    # print(paths)
                # print("\n")
        return path_list

    def findStype(self, file_dir, stype="txt"):
        """
        查找文件后缀为指定格式文件
        :param file_dir: 文件路径
        :param stype: 文件格式 默认 txt
        :return: 输出符合条件的路径列表
        """
        if isinstance(file_dir, list):
            # 判断是否为列表
            file_dirs = file_dir
        elif isinstance(file_dir, str) and os.path.exists(file_dir):
            # 判断是否为字符串，并且文件路径是否存在
            file_dirs = []
            file_dirs.append(file_dir)
        else:
            print("输入的文件路径{}不对".format(file_dir))
            return []

        values = []
        for files in file_dirs:
            if os.path.exists(files):
                filesList = files.split(".")
                if filesList[len(filesList) - 1] == stype:
                    values.append(files)
        return values

    def outfile(self, fileFront):
        """
        随机更改文件，文件，字符
        :param moveFront: 需要更改的文件、文件夹路径
        :return:
        """
        outstr = ''
        if os.path.isfile(fileFront):
            # 文件随机命名
            value = fileFront.split('.')
            outstr = "{}{}_副本{}{}{}".format(outstr, value[0], random.randint(1, 9), random.randint(0, 9),
                                            random.randint(0, 9))
            for i in range(1, len(value) - 1):
                outstr = outstr + '.' + value[i]
            outstr = "{}.{}".format(outstr, value[len(value) - 1])

        elif os.path.isdir(fileFront):
            # 文件夹随机命名
            value = fileFront.split('/')
            for i in range(0, len(value) - 1):
                outstr = outstr + value[i] + '/'
            outstr = "{}{}_副本{}{}{}".format(outstr, value[len(value) - 1], random.randint(1, 9), random.randint(0, 9),
                                            random.randint(0, 9))

        else:
            # 字符随机
            outstr = "{}_副本{}{}{}".format(fileFront, random.randint(1, 9), random.randint(0, 9), random.randint(0, 9))

        return outstr

    def movefile(self, moveFront, moveAfter):
        """
        移动文件、文件夹
        :param moveFront: 需要移动的文件、文件夹路径
        :param moveAfter: 移动后的文件、文件夹路径
        :return:
        """
        try:
            shutil.move(moveFront, moveAfter)
        except:
            print("{} 在文件 {} 已存在".format(moveFront, moveAfter))
            return moveFront

    def copyfile(self, copyFront, copyAfter, overlay=True):
        """
        复制文件、文件夹
        :param copyFront: 需要复制的文件、文件夹路径
        :param copyAfter: 复制后的文件、文件夹路径
        :param overlay: True 复制    False 覆盖复制
        :return: 无
        """

        if overlay:
            shutil.copy(copyFront, copyAfter)
        else:
            shutil.copy2(copyFront, copyAfter)

    def renamefile(self, nameFront,flag = None, nameAfter=None):
        """
        文件、文件夹重命名
        :param nameFront: 需要命名的文件、文件夹路径
        :param flag: True 根目录创建宽高  Flase 当前文件目录创建宽高
        :param nameAfter: 命名后的文件、文件夹路径
        :return: 执行
        """

        if nameAfter == None and os.path.isfile(nameFront):
            try:
                # 读取视频图片md5
                md5 = self.filemd5(nameFront)
                # 读取视频图片信息
                values = self.get_video_info(nameFront)
                # print(values)
                # 判断视频图片信息[]
                if values !=[]:
                    # 视频图片文件的目录
                    folder_path = values[0]["folder_path"]
                    width = values[0]["width"]
                    height = values[0]["height"]
                    size = values[0]["size"]
                    # 读取视频图片文件格式
                    file_format = values[0]["file_format"]
                    image_formats = ["bmp","jpeg","jpg","png","tif","gif","pcx","tga","exif","fpx","svg","psd","cdr","pcd","dxf","ufo","eps","ai","raw","WMF","webp","avif","apng"]
                    video_formats = ["mp4","mov","m4v","wmv","avi","flv"]
                    # 读取本地视频图片文件的格式
                    str_values = self.str_split(nameFront,'.')
                    # 如果读取文件后缀不为[]
                    if str_values != []:
                        Suffix = str_values[-1]
                    else:
                        Suffix = values[0]["file_format"]
                    if file_format in image_formats:
                        file_name = "image"
                    elif file_format in video_formats:
                        file_name = "video"
                    else:
                        file_name = "material"
                    # 拼接文件名称+后缀
                    name = "{}_{}_{}_{}.{}".format(file_name,width,height,md5,Suffix)
                    # 为None 当前文件目录下创建，否者给定的目录进行创建
                    if flag == None:
                        all_path = os.path.dirname(folder_path)
                    else:
                        all_path = flag
                    # 文件目录和文件宽高拼接
                    folder_paths = os.path.join(all_path,"{}_{}".format(width,height))
                    # print(folder_paths)
                    # 拼接的目录存在不进行创建，不存在进行创建
                    self.is_path(folder_paths)
                    # 文件目录+文件名称进行拼接
                    file_paths = os.path.join(folder_paths,name)
                    os.rename(nameFront,file_paths)

            except:
                pass
        else:
            # 文件夹命名
            if os.path.isdir(nameFront) and os.path.isdir(nameAfter):
                os.rename(nameFront, nameAfter)
            # 文件命名
            elif os.path.isfile(nameFront) and os.path.isfile(nameAfter):
                os.rename(nameFront, nameAfter)
            else:
                print("{} 和 {}不能进行重命名".format(nameFront, nameAfter))

    def readfile(self, file_path):
        """
        读取文件文件内容
        :param file_path: 文本文件路径
        :return: 返回文本文件内容
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                return line

        f.close()

    def writefile(self, file_path, txt, isw=False):
        """
        写文本文件
        :param file_path: 问你路径
        :param txt: 写入的文本
        :param isw: True 覆盖写入   False 追加写入
        :return: 无
        """
        if isw:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(txt)
        else:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + txt)
        f.close()

    def is_path(self, path):
        """
        判断目录是否存在，不存在就进行新建
        :param path: 文件路径
        :return: 执行
        """

        if os.path.isdir(path) == False:
            os.makedirs(path)

    def chagemd5(self, file_path):
        # 改变文件的MD5
        # filename 文件路径
        myfile = open(file_path, 'a')
        myfile.write("####&&&&")
        myfile.close

    def filemd5(self, file_path, flag=False):
        """
        读取文件MD5
        :param filename: 路径
        :param flag: 开关 True 改变MD5  False 不改变MD5 只读取MD5
        :return:返回MD5
        """

        if flag:
            self.chagemd5(file_path)
        hasher = hashlib.md5()
        with open(file_path, "rb") as file:
            buf = file.read()
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read()
        # print(hasher.hexdigest())
        return hasher.hexdigest()

    def str_split(self, data, ide='\\'):
        """
        数据中找到idt，找到返回找到的数据，没有找到返回[]
        :param data:数据源
        :param ide:按照ide对数据源切割
        :return:切割后的列表
        """
        data = str(data)
        if data.find(ide) == -1:
            return []
        else:
            value = data.split(ide)
            return value

    def str_strip(self,data,direction = "all"):
        data = str(data)
        if direction == "left":
            value = data.lstrip()
            return value
        elif direction == "right":
            value = data.rstrip()
            return value
        else:
            value = data.strip()
            return value

    def name_rand(self, name="Resource", out_file_path=None, flag=False):
        """
        文件名称拼接随机值
        :param name: 文件名称
        :param out_file_path: True 进行文件路径拼接   Flase 不进行文件路径拼接
        :param flag: True 进行拼接  Flase 不进行拼接
        :return: 输出随机命名的文件或者路径
        """

        if flag:
            file_name = "{}_{}{}{}{}".format(name, int(time.time()), random.randint(1, 9), random.randint(1, 9),
                                             random.randint(1, 9), random.randint(1, 9))
        else:
            file_name = name
        if out_file_path != None and os.path.isdir(out_file_path):
            file_name = os.path.join(out_file_path, file_name)

        return file_name

    def get_video_dimensions(self, url):
        # 通过视频ulr解析视频宽高
        video_capture = cv2.VideoCapture(url)
        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_capture.release()
        return width, height

    def get_url_md5(self, url):
        filename = url.split('/')[-1]  # 提取文件名

        response = requests.get(url)  # 发送GET请求

        md5_obj = hashlib.md5()  # 创建MD5对象
        md5_obj.update(response.content)  # 更新MD5对象

        return md5_obj.hexdigest()  # 返回MD5值

    def get_video_info(self, path):
        try:
            # 解析视频文件
            # probe = ffmpeg.probe('./测试视频文件.mp4')
            probe = ffmpeg.probe(path)
            # print(probe)  # 获取视频多媒体文件的信息
            format = probe['format']
            # print(format)

            filepath = format['filename']  # 文件路径
            # logger.info("文件路径为：{}".format(filepath))
            filenames = os.path.basename(filepath)  # 获取文件路径中的文件名称，带后缀
            filename = filenames.split(".")[0]  # 获取文件路径中的文件名称，去掉后缀
            # filename = os.path.splitext(filepath)

            folder_path = str.split(filepath, filenames)[0]  # 利用str截取字符串获取文件夹的路径

            fileformat = os.path.splitext(filepath)[1]  # 获取文件格式
            fileformat = fileformat.split(".")[1]  # 去掉圆点

            # logger.info("文件名称为：{}".format(filename))
            # logger.info("文件格式为：{}".format(fileformat))

            bit_rate = format['bit_rate']
            # print("比特率(bps)为:{}".format(int(bit_rate)))  # 单位 bps（每秒字节数）
            kbps = int(bit_rate) / 1000
            kbps = round(kbps)
            # logger.info("比特率为(kbps):{}".format(kbps))  # 单位 kbps（每秒字节数）kbps

            fps_a = int(probe['streams'][0]['r_frame_rate'].split('/')[0])
            fps_b = int(probe['streams'][0]['r_frame_rate'].split('/')[1])
            fps = fps_a / fps_b  # 获取帧率
            fps = round(fps)
            # logger.info("视频帧率为：{}".format(fps))

            streams = probe['streams'][0]
            width = streams['width']
            coded_width = streams['coded_width']
            height = streams['height']
            coded_height = streams['coded_height']
            # logger.info("视频宽为(px)：{}".format(width))
            # logger.info("视频高为(px)：{}".format(height))

            duration = format['duration']
            duration = round(float(duration), 2)  # 时长（单位秒）
            # logger.info("时长为(s)：{}".format(duration))

            # 通过比特率X时长/8 计算文件大小，不是很准确
            # file_size = kbps * duration / 8
            # print("通过比特率X时长/8 计算文件大小:{}kb".format(file_size))  # 得到文件的大小是 KB
            # print("通过比特率X时长/8/1024 计算文件大小:{}M".format(file_size / 1024))  # 计算得到的数据

            size_b = int(format['size'])  # 获取文件大小（单位字节B）
            size_kb = float(format['size']) / 1024  # 获取文件大小（单位字节KB）
            size = float(format['size']) / 1024 / 1024  # 获取文件大小（单位字节M）
            size = round(size, 2)  # 文件大小保留两位小数
            size_kb = round(size_kb, 2)  # 文件大小保留两位小数
            # logger.info("文件大小为(b)：{}".format(size_b))
            # logger.info("文件大小为(kb)：{}".format(size_kb))
            # logger.info("文件大小为(m)：{}".format(size))

            title = {"folder_path": "文件夹路径", "file_path": "文件路径", "file_name": "文件名称", "file_format": "文件后缀",
                     "kbps": "比特率(kbps)", "fps": "视频帧率", "width": "视频宽(px)", "height": "视频高(px)", "duration": "时长(s)",
                     "size_b": "文件大小(b)", "size_kb": "文件大小(kb)", "size": "文件大小(m)"}
            # logger.info("输出所有字段为：\n{}".format(title))
            dict_list = {}
            # dict_list["title"] = title
            dict_list["folder_path"] = folder_path
            dict_list["file_path"] = filepath
            dict_list["file_name"] = filename
            dict_list["file_format"] = fileformat
            dict_list["kbps"] = kbps
            dict_list["fps"] = fps
            dict_list["width"] = width
            dict_list["height"] = height
            dict_list["duration"] = duration
            dict_list["size_b"] = size_b
            dict_list["size_kb"] = size_kb
            dict_list["size"] = size
            lists = []
            lists.append(dict_list)
        except:
            # logger.info("文件异常：{}".format(path))
            return None
        return (lists)

    def file_info(self,input_path,out_path):
        """
        提取文件信息进行返回
        :param input_path: 输入文件信息
        :return: 返回文件信息

         目前全部字段，前三个一定返回
        ["name","path","format","md5","width","height","duration","size_b","size_kb","size"]
        """
        lock.acquire()
        image_formats = ["bmp", "jpeg", "jpg", "png", "tif", "gif", "pcx", "tga", "exif", "fpx", "svg", "psd", "cdr",
                         "pcd", "dxf", "ufo", "eps", "ai", "raw", "WMF", "webp", "avif", "apng"]
        video_formats = ["mp4", "mov", "m4v", "wmv", "avi", "flv"]
        material_formats  = image_formats + video_formats



        # 存放返回数据
        data_list = []
        # print(material_formats)
        # 文件名
        file_name = self.str_split(input_path)[-1]
        new_name = self.str_split(file_name,'.')
        if new_name != []:
            txt = ''
            if len(new_name) > 2:
                # 减1为了去除后缀，可能文件名有多个.所以用for
                txt = new_name[0]
                for i in range(1,len(new_name)-1):
                    txt = "{}.{}".format(txt,new_name[i])
            else:
                txt = new_name[0]
            file_name = self.str_strip(txt)

        # 文件后缀
        file_format = self.str_split(input_path,'.')[-1]
        # 文件md5
        md5 = self.filemd5(input_path)

        data_list.append(file_name)
        data_list.append(input_path)
        data_list.append(file_format)
        data_list.append(md5)

        if file_format in material_formats:
            try:
                # 素材信息
                material_info = self.get_video_info(input_path)[0]
                # print(material_info)
                width = material_info["width"]
                height = material_info["height"]
                duration = material_info["duration"]
                size_b = material_info["size_b"]
                size_kb = material_info["size_kb"]
                size = material_info["size"]

                data_list.append(width)
                data_list.append(height)
                data_list.append(duration)
                data_list.append(size_b)
                data_list.append(size_kb)
                data_list.append(size)
            except:
                codes = str({"msg":"读取视频信息错误"})
                data_list.append(codes)
                pass



        if os.path.isfile(out_path):
            csv_path = os.path.dirname(out_path)
            csv_name = self.str_split(out_path)[-1]
            mycsv = MyCsv(csv_path,csv_name,"gbk")
            mycsv.dowriteList(data_list)

        lock.release()


class MultiConcurrence(MyOs):
    def multi_move_file(self, input_path, out_path, num=3):
        """
        文件、文件夹移动
        :param input_path: 移动文件、文件夹前路径
        :param out_path: 移动文件、文件夹后路径
        :param num: 并发数
        :return: 执行
        """
        values = self.filelist(input_path)
        self.multi_thread(self.movefile, values, num, out_path)

    def multi_copy_file(self, input_path, out_path, num=3):
        """
        文件、文件夹拷贝
        :param input_path: 拷贝文件、文件夹前路径
        :param out_path: 拷贝文件、文件夹后路径
        :param num: 并发数
        :return: 执行
        """
        values = self.filelist(input_path)
        self.multi_thread(self.copyfile, values, num, out_path)

    def multi_rename_file(self, input_path, out_path=None, num=3, flag = False):
        """
        文件、文件夹重命名
        :param input_path:命名前的文件、文件夹
        :param out_path:明确的命名文件、文件夹
        :param num: 并发数
        :param flag: 指定的文件夹下
        :return: 执行
        """
        values = self.filelist(input_path)
        if flag == False:
            self.multi_thread(self.renamefile, values, num)
        else:
            self.multi_thread(self.renamefile,values,num,input_path)

    def multi_get_path_write_csv(self,input_path,out_path = None,file_name = None, num=3,flag = False):

        if out_path == None:
            out_path = input_path
        if file_name == None:
            name = "StatisticalPath.csv"
        else:
            name = file_name
        file_path = os.path.join(out_path,name)
        title_flag = os.path.isfile(file_path)

        mycsv = MyCsv(out_path,name)
        if flag == False or title_flag == False:
            mycsv.title("name","path","format","md5","width","height","duration","size_b","size_kb","size_m")

        datas = self.filelist(input_path)
        self.multi_thread(self.file_info,datas,num,file_path)
