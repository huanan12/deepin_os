import os
import shutil
import random

class MyOs():
    def filelist(self,file_dir):
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
        for root,dirs,files in os.walk(file_dir):
            #root 根目录
            #dirs 子目录
            #files 子目录文件
            #主要拉出根路径的文件
            if root == file_dir and dirs != []:
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

    def findStype(self,file_dir,stype = "txt"):
        """
        查找文件后缀为指定格式文件
        :param file_dir: 文件路径
        :param stype: 文件格式 默认 txt
        :return: 输出符合条件的路径列表
        """
        if isinstance(file_dir,list):
            # 判断是否为列表
            file_dirs = file_dir
        elif isinstance(file_dir,str) and os.path.exists(file_dir):
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
                if filesList[len(filesList)-1] == stype:
                    values.append(files)
        return values

    def outfile(self,fileFront):
        """
        随机更改文件，文件，字符
        :param moveFront: 需要更改的文件、文件夹路径
        :return:
        """
        outstr = ''
        if os.path.isfile(fileFront):
            # 文件随机命名
            value = fileFront.split('.')
            outstr = "{}{}_副本{}{}{}".format(outstr,value[0],random.randint(1,9),random.randint(0,9),random.randint(0,9))
            for i in range(1,len(value)-1):
                outstr = outstr + '.' + value[i]
            outstr = "{}.{}".format(outstr,value[len(value)-1])

        elif os.path.isdir(fileFront):
            # 文件夹随机命名
            value = fileFront.split('/')
            for i in range(0,len(value)-1):
                outstr = outstr + value[i] + '/'
            outstr = "{}{}_副本{}{}{}".format(outstr,value[len(value)-1], random.randint(1, 9), random.randint(0, 9),random.randint(0, 9))

        else:
            # 字符随机
            outstr = "{}_副本{}{}{}".format(fileFront,random.randint(1, 9), random.randint(0, 9),random.randint(0, 9))


        return outstr

    def movefile(self,moveFront,moveAfter):
        """
        移动文件、文件夹
        :param moveFront: 需要移动的文件、文件夹路径
        :param moveAfter: 移动后的文件、文件夹路径
        :return:
        """
        try:
            shutil.move(moveFront, moveAfter)
        except:
            print("{} 在文件 {} 已存在".format(moveFront,moveAfter))
            return moveFront

    def copyfile(self,copyFront,copyAfter,overlay = True):
        """
        复制文件、文件夹
        :param copyFront: 需要复制的文件、文件夹路径
        :param copyAfter: 复制后的文件、文件夹路径
        :param overlay: True 复制    False 覆盖复制
        :return: 无
        """
        if overlay:
            shutil.copy(copyFront,copyAfter)
        else:
            shutil.copy2(copyFront, copyAfter)

    def renamefile(self,nameFront,nameAfter):
        """
        文件、文件夹重命名
        :param nameFront: 需要命名的文件、文件夹路径
        :param nameAfter: 命名后的文件、文件夹路径
        :return: 无
        """
        if os.path.isdir(nameFront) and os.path.isdir(nameAfter):
            os.rename(nameFront,nameAfter)
        elif os.path.isfile(nameFront) and os.path.isfile(nameAfter):
            os.rename(nameFront, nameAfter)
        else:
            print("{} 和 {}不能进行重命名".format(nameFront,nameAfter))

    def readfile(self,file_path):
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

    def writefile(self,file_path,txt,isw = False):
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
                f.write("\n"+txt)
        f.close()

myos = MyOs()


if __name__ == "__main__":

    # newpath = r"E:\orpath"
    # newpath = r"E:\orpath\twos"
    # path = r"E:\orpath\newpath"
    # values = myos.filelist(newpath)
    # fileos = myos.findStype(values)
    # for i in fileos:
    #     myos.movefile(i,path)
    #
    # path = r"E:\orpath\twos\9\评语.txt"
    # path = r"E:\orpath\twos\9"
    # path = r"twos"
    # newpath = myos.outfile(path)
    # txt = myos.readfile(path)
    # txt = myos.writefile(path,"word")
    # txt = myos.readfile(path)
    # print(txt)
    # print(myos.outfile(path))



    pass
