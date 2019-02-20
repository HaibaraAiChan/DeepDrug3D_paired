#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Predict the protein binds to ATP or Heme

@author: Limeng Pu
"""

import sys
import argparse

from voxelization import Vox3DBuilder

from keras.models import load_model

def myargs():
    parser = argparse.ArgumentParser()                                              
    parser.add_argument('--protein', 
			required = False,
			default='../ATP/Proteins/1abiA.pdb', 
			help ='location of the protein pdb file path')
    parser.add_argument('--aux',
			required = False,
			default='../ATP/aux_files/1abiA_aux.txt',
			help ='location of the auxilary input file')
    parser.add_argument('--r', 
			required = False, 
			help ='radius of the grid to be generated',
			default=15,
                       type=int, dest='r')
    parser.add_argument('--N', required = False, help = 
                        'number of points long the dimension the generated grid', default=31,
                       type=int, dest='N')
    args = parser.parse_args()
    return args



def main(protein_path, aux_path, r, N):
    voxel = Vox3DBuilder.voxelization(protein_path, aux_path, r, N)
    mdl = load_model('deepdrug3d.h5')
    score = mdl.predict(voxel)
    print('************************The probability of biniding with ATP: ' + str(score[0]))
    print('************************The probability of biniding with Heme: ' + str(score[1]))
    
if __name__ == "__main__":
    args = myargs()
    main(args.protein, args.aux, args.r, args.N)
