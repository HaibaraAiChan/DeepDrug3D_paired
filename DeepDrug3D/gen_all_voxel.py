import sys
import os
import argparse
import numpy as np
import shutil
import cPickle
from voxelization import Vox3DBuilder
import warnings
warnings.filterwarnings("ignore")

def myargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protein',
                        required=False,
                        default='../ATP/Proteins/',
                        help='location of the protein pdb file path')
    parser.add_argument('--aux',
                        required=False,
                        default='../ATP/aux_files/',
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


def gen_one_voxel(protein_path, aux_path, output, r, N):
    voxel = Vox3DBuilder.voxelization(protein_path, aux_path, r, N)
    print "the type of voxel data--------------------------------"
    print type(voxel)
    print voxel.shape
    print "the type of voxel data--------------------------------"
    if not os.path.exists(output):
        os.makedirs(output)
    outname = os.path.splitext(os.path.basename(aux_path))[0][0:-4]
    
    oname = output + outname + ".pkl"
    if os.path.exists(oname):
        os.remove(oname)
    cPickle.dump(voxel, open(oname, "wb"))
    Y = cPickle.load(open(oname, "rb"))
    print Y[0][0][0][0]

    print('The end of one file ')


if __name__ == "__main__":
    args = myargs()

    protein_path = args.protein
    aux_path = args.aux
    aux_filename_list = []

    for aux_file in os.listdir(aux_path):
        if aux_file:
            aux_filename_list.append(aux_file)
    print "the number of aux files is "+str(len(aux_filename_list))
    for pro_file in os.listdir(protein_path):
        base = pro_file[0:-4]
        tmp_aux_files = [aux_f for aux_f in aux_filename_list if base in aux_f]
        for au in tmp_aux_files:
            print "protein file: "+pro_file
            print "aux_file:     "+au

            gen_one_voxel(protein_path+pro_file, aux_path+au, args.output, args.r, args.N)
