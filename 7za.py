import os, os.path
import zipfile


# def zip_dir(dirname, zipfilename):
#     filelist = []
#     if os.path.isfile(dirname):
#         filelist.append(dirname)
#     else:
#         for root, dirs, files in os.walk(dirname):
#             for name in files:
#                 filelist.append(os.path.join(root, name))
#
#     zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
#     for tar in filelist:
#         arcname = tar[len(dirname):]
#         # print arcname
#         zf.write(tar, arcname)
#     zf.close()


if __name__ == '__main__':
    dirname = '/home/yulijun/tag_sys/flowers_data'
    dirs = os.listdir(dirname)
    for dir in dirs:
        if dir != '__MACOSX':
            cDir = os.path.join(dirname, dir)
            zipfilename = os.path.join(dirname, dir + '.7z')
            # print cDir, zipfilename
            str = '7za a %s %s' % (zipfilename, cDir)
            # print str
            os.system(str)

            # print cDir
            # print zipfilename
            # zip_dir(cDir, zipfilename)
    # for root, dirs, files in os.walk(dirname):
    #     print root
    #     print dirs
        # for name in dirs:
        #     print name