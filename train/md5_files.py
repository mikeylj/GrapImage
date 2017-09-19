# -*- coding: utf-8 -*-

# python 检测文件MD5值
# python version 2.6

import hashlib
import os, sys


# 简单的测试一个字符串的MD5值
def GetStrMd5(src):
    m0 = hashlib.md5()
    m0.update(src)
    print m0.hexdigest()
    pass


# 大文件的MD5值
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        # print(hash)
        return hash


if __name__ == "__main__":
    if len(sys.argv) == 2:
        files_md5   = []
        pathName = sys.argv[1]
        for dir_path, dir_names, file_names in os.walk(pathName):
            for filename in file_names:
                file = os.path.join(dir_path, filename)
                # print file
                h = CalcMD5(file)
                if not h in files_md5:
                    files_md5.append(h);
                else:
                    print file, h

    # hashfile = sys.argv[1]
        # if not os.path.exists(hashfile):
        #     hashfile = os.path.join(os.path.dirname(__file__), hashfile)
        #     if not os.path.exists(hashfile):
        #         print("cannot found file")
        #     else:
        #         CalcMD5(hashfile)
        # else:
        #     CalcMD5(hashfile)
        #     # raw_input("pause")
    else:
        print("no filename")