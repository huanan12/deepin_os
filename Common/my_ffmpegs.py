"""
ReadFfmpeg               ffmpeg处理类
get_video_info          读取视频的信息（宽高大小）
file_name_all           拉出根目录下的所有文件
image_spli              图片添加水印
image_x                 横向拼接图片
image_y                 纵向拼接图片
duration_video          视频时长裁剪
tailor_video            指定尺寸裁剪，裁剪要比原视频小
size_video              缩放视频
convert_ts_video        视频转换为.ts格式 用于视频拼接中转格式
concat_video            两个视频拼接
get_video_music         提取视频中的音乐
get_unvideo             剔除视频中音乐
merge_video_music       合并音频（纯音乐，m4a格式）和视频（纯视频，没有音乐）文件
concat_music            合并音乐，未生效
"""
import ffmpeg
import os
from Common.do_path import logs_path
from Common.my_logger import logger
from Common.mytime import MyMath

my_math = MyMath()

class ReadFfmpeg:
    def get_video_info(self,path):
        try:
            # 解析视频文件
            # probe = ffmpeg.probe('./测试视频文件.mp4')
            probe = ffmpeg.probe(path)
            # print(probe)  # 获取视频多媒体文件的信息
            format = probe['format']
            # print(format)

            filepath = format['filename'] #文件路径
            logger.info("文件路径为：{}".format(filepath))
            filenames = os.path.basename(filepath) #获取文件路径中的文件名称，带后缀
            filename = filenames.split(".")[0] #获取文件路径中的文件名称，去掉后缀
            # filename = os.path.splitext(filepath)

            folder_path = str.split(filepath,filenames)[0]    #利用str截取字符串获取文件夹的路径

            fileformat = os.path.splitext(filepath)[1]  # 获取文件格式
            fileformat = fileformat.split(".")[1]  # 去掉圆点

            logger.info("文件名称为：{}".format(filename))
            logger.info("文件格式为：{}".format(fileformat))

            bit_rate = format['bit_rate']
            # print("比特率(bps)为:{}".format(int(bit_rate)))  # 单位 bps（每秒字节数）
            kbps = int(bit_rate) / 1000
            kbps = round(kbps)
            logger.info("比特率为(kbps):{}".format(kbps))  # 单位 kbps（每秒字节数）kbps

            fps_a = int(probe['streams'][0]['r_frame_rate'].split('/')[0])
            fps_b = int(probe['streams'][0]['r_frame_rate'].split('/')[1])
            fps = fps_a/fps_b  # 获取帧率
            fps = round(fps)
            logger.info("视频帧率为：{}".format(fps))

            streams = probe['streams'][0]
            width = streams['width']
            coded_width = streams['coded_width']
            height = streams['height']
            coded_height = streams['coded_height']
            logger.info("视频宽为(px)：{}".format(width))
            logger.info("视频高为(px)：{}".format(height))

            duration = format['duration']
            duration = round(float(duration),2)  # 时长（单位秒）
            logger.info("时长为(s)：{}".format(duration))

            # 通过比特率X时长/8 计算文件大小，不是很准确
            # file_size = kbps * duration / 8
            # print("通过比特率X时长/8 计算文件大小:{}kb".format(file_size))  # 得到文件的大小是 KB
            # print("通过比特率X时长/8/1024 计算文件大小:{}M".format(file_size / 1024))  # 计算得到的数据

            size_b = int(format['size']) # 获取文件大小（单位字节B）
            size_kb = float(format['size'])/1024 # 获取文件大小（单位字节KB）
            size = float(format['size'])/1024/1024 # 获取文件大小（单位字节M）
            size = round(size,2) #文件大小保留两位小数
            size_kb = round(size_kb,2) #文件大小保留两位小数
            logger.info("文件大小为(b)：{}".format(size_b))
            logger.info("文件大小为(kb)：{}".format(size_kb))
            logger.info("文件大小为(m)：{}".format(size))

            title = {"folder_path":"文件夹路径","file_path":"文件路径","file_name":"文件名称","file_format":"文件后缀","kbps":"比特率(kbps)","fps":"视频帧率","width":"视频宽(px)","height":"视频高(px)","duration":"时长(s)","size_b":"文件大小(b)","size_kb":"文件大小(kb)","size":"文件大小(m)"}
            logger.info("输出所有字段为：\n{}".format(title))
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
            logger.info("文件异常：{}".format(path))
            return None
        return(lists)

    def file_name_all(self,file_dir):
        #拉出根目录下的所有文件
        path_list = []
        for root,dirs,files in os.walk(file_dir):
            #root 根目录
            #dirs 子目录
            #files 子目录文件
            #主要拉出根路径的文件
            if root == file_dir:
                # print(root)
                for i in range(len(files)):
                    paths = os.path.join(root,files[i])
                    path_list.append(paths)
                    # print(paths)
                # print("\n")
            #主要拉出根目录下的所有子目录的文件
            if dirs == []:
                # print('目录路径    ：',root)
                # print('子目录名称  ：',dirs)
                # print('目录下的文件：',files)
                # print("\n")
                # print(root)
                for i in range(len(files)):
                    paths = os.path.join(root,files[i])
                    path_list.append(paths)
                    # print(paths)
                # print("\n")
        return path_list

    def image_spli(file_path, png_path, org_path):
        # 图片添加水印
        """
        file_path: 原图片地址
        png_path: 水印图片地址
        org_path: 输出图片地址

        """
        dosc = "ffmpeg -i {} -i {} -filter_complex \"overlay=0:0\" -y {}".format(str(file_path), str(png_path),
                                                                                 str(org_path))
        os.system(dosc)

    def image_x(file_path, png_path, org_path):
        """
        # 横向拼接图片
        file_path: 第一图片地址
        png_path: 第二张图片地址
        org_path: 输出图片地址

        """
        dosc = "ffmpeg -i {} -i {} -filter_complex hstack -y {}".format(str(file_path), str(png_path), str(org_path))
        os.system(dosc)

    def image_y(file_path, png_path, org_path):
        """
        纵向拼接图片
        file_path: 第一图片地址
        png_path: 第二张图片地址
        org_path: 输出图片地址

        """
        dosc = "ffmpeg -i {} -i {} -filter_complex vstack -y {}".format(str(file_path), str(png_path), str(org_path))
        os.system(dosc)

    def duration_video(self,paths,ends,stra = 2,file_name = "output.mp4",flag = False):
        """
        时长裁剪
        :param paths: 原视频路径
        :param ends: 裁剪多少s  列如 60
        :param stra: 从视频的多少s开始裁剪   例如 5s开始裁剪
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return: 执行操作
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"
        # 分钟处理
        minute = int(ends/60)
        stra_minute = int(stra/60)
        # 秒钟处理
        second = int(ends) % 60
        stra_second = int(stra) % 60
        if stra_minute >= 0 and stra_minute < 10:
            stra_minute = "0{}".format(stra_minute)
        if stra_second >= 0 and stra_second < 10:
            stra_second = "0{}".format(stra_second)
        if stra >= 0 and minute < 10:
            minute = "0{}".format(minute)
        if second >= 0 and second < 10:
            second = "0{}".format(second)

        stra_time = "{}:{}.000".format(stra_minute,stra_second)
        end_time = "{}:{}.000".format(minute,second)

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath,file_name)

        sys ="ffmpeg -i {} -ss {} -to {} -vcodec copy -acodec copy -y {}".format(paths,stra_time,end_time,org_path)
        os.system(sys)
        return org_path

    def tailor_video(self,paths,width,height,x = 0,y = 0,file_name = "output.mp4",flag = False):
        """
        指定尺寸裁剪，裁剪要比原视频小
        :param paths: 原视频路径
        :param width: 裁剪宽
        :param height: 裁剪高
        :param x: x轴
        :param y: y轴
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"
        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i {} -strict -2 -vf crop={}:{}:{}:{} -c:v libx264 -y {}".format(paths,int(width),int(height),int(x),int(y),org_path)
        os.system(sys)
        return org_path

    def size_video(self,paths,width,height,file_name = "output.mp4",flag = False):
        """
        缩放视频
        :param paths: 原视频路径
        :param width: 缩放宽
        :param height: 缩放高
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"
        width = int(width)
        height = int(height)
        # 公约数 x/y 比例
        divisor = my_math.gdc(width,height)
        x = int(width / divisor)
        y = int(height / divisor)

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i {} -vf scale={}:{},setdar={}/{} -y {}".format(paths,width,height,x,y,org_path)
        os.system(sys)
        return org_path

    def convert_ts_video(self, paths, file_name="1.ts", flag=False):
        """
        视频转换为.ts格式
        :param paths: 原视频路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i concat:{} -vcodec copy -acodec copy -vbsf h264_mp4toannexb -y {}".format(paths,org_path)
        os.system(sys)
        return org_path

    def concat_video(self,paths,pathsone, file_name="output.mp4", flag=False):
        """
        两个视频拼接
        :param paths: 原视频1路径
        :param paths: 原视频2路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        value1 = self.convert_ts_video(paths,"1.ts")
        value2 = self.convert_ts_video(pathsone,"2.ts")
        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = 'ffmpeg -i "concat:{}|{}" -acodec copy -vcodec copy -absf aac_adtstoasc -y {}'.format(value1,value2,org_path)
        os.system(sys)
        os.remove(value1)
        os.remove(value2)
        return org_path

    def get_video_music(self,paths, file_name="output.m4a", flag=False):
        """
        视频提起音频m4a文件
        :param paths: 原视频路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i {} -vn -acodec copy -y {}".format(paths,org_path)
        os.system(sys)
        return org_path

    def get_unvideo(self,paths, file_name="output.mp4", flag=False):
        """
        视频剔除mp3音频
        :param paths: 原视频路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i {} -an -vcodec copy -y {}".format(paths,org_path)
        os.system(sys)
        return org_path

    def merge_video_music(self,paths ,pathsone, file_name="output.mp4", flag=False):
        """
        合并音视频
        :param paths: 原视频路径
        :param pathsone: 原音频路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        sys = "ffmpeg -i {} -i {} -c copy -y {}".format(paths,pathsone,org_path)
        logger.info(sys)
        os.system(sys)
        return org_path

    def concat_music(self,paths,pathsone, file_name="output.mp3", flag=False):
        """
        合并两段音频 （不生效）
        :param paths: 原音频1路径
        :param pathsone: 原音频2路径
        :param file_name:输出名称 需要带上后缀
        :param flag: 开关，开：file_name为完整路径名称  关：文件名称
        :return:
        """
        if os.path.isfile(paths) == False:
            print("不是文件")
            return "不是文件"

        # flag true file_name传的是完整路径   false 传的是文件名
        if flag:
            org_path = file_name
        else:
            orgpath = os.path.dirname(paths)
            org_path = os.path.join(orgpath, file_name)
        # "ffmpeg -i input1.mp3 -i input2.mp3 -filter_complex amerge -ac 2 -c:a libmp3lame -q:a 4 output.mp3"
        # sys = "ffmpeg -i {} -i {} -c:a aac -strict experimental -y {}".format(paths,pathsone,org_path)
        sys = "ffmpeg -i {} -i {} -filter_complex amerge -ac 2 -c:a aac -q:a 4 -y {}".format(paths,pathsone,org_path)
        os.system(sys)
        return org_path
readffmpeg = ReadFfmpeg()

if __name__ == '__main__':
    # get_video_info()
    # path = r"C:\Users\v_ghuachen\Documents\VeryCapture"
    # path = r"D:\大创意\大创意\视频\正常时长\case1\9-16\720-1280"
    # path = os.path.abspath(__file__)

    # files = os.listdir(path)
    # for i in range(len(files)):
    # # for i in range(1):
    #     paths = os.path.join(path,files[i])
    #     value = readffmpeg.get_video_info(paths)
        # print(value[0]["width"])
        # print(value)

    # paths = "D:/media/new_media_two_two/media_1670942056.mp4"
    # paths = "D:/media/new_media_two_two\output.mp4"
    # paths2 = "D:/media/new_media_two_two\output.m4a"
    # readffmpeg.duration_video(paths,60,0)
    # readffmpeg.tailor_video(paths,100,800,100,100)
    # readffmpeg.size_video(paths,1080,1920)
    # value1 = readffmpeg.convert_ts_video(paths,"1.ts")
    # value1 = readffmpeg.concat_video(paths,paths)
    # value1 = readffmpeg.get_video_music(paths)
    # value1 = readffmpeg.get_unvideo(paths)
    # value1 = readffmpeg.concat_music(paths2,paths2,"out.mp3")
    # value1 = readffmpeg.merge_video_music(paths,paths2,"out.mp4")
    # print(value1)
    path = r"D:\linshi\output_7_19.mp4"
    paths = r"D:\linshi\output2_720.mp4"
    outpaths = r"D:\linshi\output_7_720.mp4"
    # readffmpeg.concat_video(paths,path, outpaths, True)
    readffmpeg.duration_video(path,6, 0,outpaths, True)




    # path_all = readffmpeg.file_name_all(path)
    # for i in range(len(path_all)):
    #     print(path_all[i])
