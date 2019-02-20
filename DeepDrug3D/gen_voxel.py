import sys
import os
import argparse
import numpy as np
import shutil
import cPickle
from voxelization import Vox3DBuilder
#
# from keras.models import load_model


def myargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protein',
                        required=False,
                        default='../ATP/Proteins/1abiA.pdb',
                        help='location of the protein pdb file path')
    parser.add_argument('--aux',
                        required=False,
                        default='../ATP/aux_files/1abiA_DPN_aux.txt',
                        help='location of the auxilary input file')
    parser.add_argument('--r',
                        required=False,
                        help='radius of the grid to be generated',
                        default=15,
                        type=int,
                        dest='r')
    parser.add_argument('--N',
                        required=False,
                        help='number of points long the dimension the generated grid',
                        default=31,
                        type=int,
                        dest='N')
    parser.add_argument('--output',
                        required=False,
                        default='./voxel_output/',
                        help='location of the protein pdb file path')
    args = parser.parse_args()
    return args


def main(protein_path, aux_path, output, r, N):
    voxel = Vox3DBuilder.voxelization(protein_path, aux_path, r, N)
    print "the type of voxel data--------------------------------"
    print type(voxel)
    print voxel.shape
    print "the type of voxel data--------------------------------"
    if not os.path.exists(output):
	os.makedirs(output)
    filename=os.path.splitext(os.path.basename(protein_path))[0]
    oname=output+filename+"_out.pkl"
    if os.path.exists(oname):
	os.remove(oname)
    cPickle.dump(voxel,open(oname,"wb"))
    Y=cPickle.load(open(oname,"rb"))
    print Y

#    f = open(output+filename+"_out.txt",'w')
 #   f.write(voxel)
  #  f.close()
    print('The end of one file ')


if __name__ == "__main__":
    args = myargs()
    main(args.protein, args.aux, args.output, args.r, args.N)
