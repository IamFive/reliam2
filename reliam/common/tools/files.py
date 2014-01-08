# -*- coding: utf-8 -*-
#
# @author: Woo Cupid
# Created on 2013-5-14
# Copyright (c) 2011-2013 Woo cupid(iampurse#vip.qq.com)
#
import os
import zipfile
import csv
import logging

def headn(path, n=5):
    """Like *x head -N command"""
    result = []
    nlines = 0
    assert n >= 1
    with open(path, 'rU') as f:
        for line in f:
            result.append(line)
            nlines += 1
            if nlines >= n:
                break
    return result

def get_csv_dialect(path):
    zip_path = path
    samples = headn(zip_path, 6)
    sniffer = csv.Sniffer()
    try:
        with open(path, 'rU') as f:
            dialect = sniffer.sniff(f.read(1024),
                                    delimiters=[',', '\t', ' ', ':', ';', '|'])
    except Exception, e:
        logging.info('cant detect delimiter for csv line: ' + samples[-1])
        dialect = None
    return samples, dialect


def zip_dir(dirname, zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, _, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
        
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()


def unzip_file(zipfilename, unziptodir):
    if not os.path.exists(unziptodir): os.mkdir(unziptodir, 0777)
    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace('\\', '/')
       
        if name.endswith('/'):
            os.mkdir(os.path.join(unziptodir, name))
        else:            
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir) : os.mkdir(ext_dir, 0777)
            outfile = open(ext_filename, 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()

if __name__ == '__main__':
    zip_dir(r'E:/python/learning', r'E:/python/learning/zip.zip')
    unzip_file(r'E:/python/learning/zip.zip', r'E:/python/learning2')
