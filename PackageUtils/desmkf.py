#!/usr/bin/env python2
# -*- coding: utf-8 -*-  
import argparse
import struct
import os

def deMKF(f,postfix):
    mkf_name=os.path.basename(f.name)
    prefix=os.path.splitext(mkf_name)[0]
    f.seek(0,os.SEEK_END)
    total_length=f.tell()
    f.seek(0,os.SEEK_SET)
    packarg="<H" if use_unsigned_short else "<h"
    first_index, = struct.unpack(packarg,f.read(2))
    subfiles = first_index-1
    for i in range(0,subfiles):
        with open(prefix+str(i)+"."+postfix, 'wb') as subfile:
            f.seek(i*2,os.SEEK_SET)
            begin,  = struct.unpack(packarg,f.read(2))
            end,    = struct.unpack(packarg,f.read(2))
            begin   = begin if begin > 0 else 32768+begin
            end     = end   if end   > 0 else 32768+end
            end     = end   if end  != 0 else total_length/2
            f.seek(begin*2,os.SEEK_SET)
            subfile.write(f.read(end*2-begin*2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sMKF unpack util')
    parser.add_argument('sMKF', type=argparse.FileType('rb'), action="store",
                       help='sMKF file to unpack')
    parser.add_argument('-p','--postfix', required=True,
                       help='postfix for unpacked files')

    args = parser.parse_args()
    use_unsigned_short = True if os.path.getsize(args.sMKF.name) > 64 * 1024 else False
    deMKF(args.sMKF,args.postfix)