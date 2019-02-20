import sys
import os
import argparse

import numpy as np

from deepdrug3d import DeepDrug3DBuilder

from keras import callbacks
from keras.optimizers import Adam
from keras.utils import np_utils
import cPickle


def myargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pos_list',
                        required=False,
                        default='./pos.lst', #/pos-new-ATP.lst',
                        help='pos-new-ATP.lst')
    parser.add_argument('--neg_list',
                        required=False,
                        default='./neg.lst', #/neg-new-ATP.lst',
                        help='neg-new-ATP.lst')
    parser.add_argument('--vfolder',
                        required=False,
                        default='./voxel_data/',
                        help='folder for the voxel data')
    parser.add_argument('--bs',
                        required=False,
                        default=32,
                        help='batch size')
    parser.add_argument('--lr',
                        required=False,
                        default=0.1,
                        help='initial learning rate')
    parser.add_argument('--epoch',
                        required=False,
                        default=1,
                        help='number of epochs for taining')
    parser.add_argument('--output',
                        required=False,
                        default='./output_DP/',
                        help='location for the model to be saved')
    args = parser.parse_args()
    return args





def pre_pro_data(pos_list, neg_list, voxel_folder):

    voxel_name_list = []
    for filename in os.listdir(voxel_folder):
        if filename:
            voxel_name_list.append(filename[0:-4])
    pos = []
    with open(pos_list) as atp_in:
        for line in atp_in.readlines():
            temp = line.replace(' ', '').replace('\n', '')
            pos.append(temp)
    neg = []
    with open(neg_list) as heme_in:
        for line in heme_in.readlines():
            temp = line.replace(' ', '').replace('\n', '')
            neg.append(temp)
    # convert data into a single matrix
    pos_len = len(pos)
    neg_len = len(neg)
    L = pos_len + neg_len

    voxel_list=[]
    # one_voxel = np.zeros(shape=(28, 32, 32, 32), dtype=np.float64)
    label = []
    # cnt = 0

    print('...list pos')
    for p1 in pos:
        pp = p1.split('_')
        pocket1 = pp[0]+'_'+pp[1]
        pocket2 = pp[2]+'_'+pp[3]
        assert any(pocket1 in voxel for voxel in voxel_name_list)
        assert any(pocket2 in voxel for voxel in voxel_name_list)

        full_path_1 = voxel_folder + '/' + pocket1+'.pkl'
        full_path_2 = voxel_folder + '/' + pocket2+'.pkl'

        temp1 = np.load(full_path_1)
        temp2 = np.load(full_path_2)
        temp = np.append(temp1, temp2, axis=1)

        voxel_list.append(temp)
        label.append(int(1))
    print('...List neg')
    for p1 in neg:
        pp = p1.split('_')
        pocket1 = pp[0]+'_'+pp[1]
        pocket2 = pp[2]+'_'+pp[3]
        assert any(pocket1 in voxel for voxel in voxel_name_list)
        assert any(pocket2 in voxel for voxel in voxel_name_list)

        full_path_1 = voxel_folder + pocket1+'.pkl'
        full_path_2 = voxel_folder + pocket2+'.pkl'

        temp1 = np.load(full_path_1)
        temp2 = np.load(full_path_2)
        temp = np.append(temp1, temp2, axis=1)

        voxel_list.append(temp)
        label.append(int(0))

    tmp =voxel_list[0]
    for i in range(len(voxel_list)-1):
        tmp=np.append(tmp,voxel_list[i+1],axis=0)



    return tmp, label


def train_deepdrug(pos_list, neg_list, voxel_folder, batch_size, lr, epoch, output):
    mdl = DeepDrug3DBuilder.build()
    adam = Adam(lr=lr, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

    # We add metrics to get more results you want to see
    mdl.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    voxel_data, label = pre_pro_data(pos_list, neg_list, voxel_folder)


    y = np_utils.to_categorical(label, num_classes=2)
    # callback function for model checking
    tfCallBack = callbacks.TensorBoard(log_dir='./graph',
                                       histogram_freq=0,
                                       batch_size=batch_size,
                                       write_graph=True,
                                       write_grads=False,
                                       write_images=True,
                                       embeddings_freq=0,
                                       embeddings_layer_names=None,
                                       embeddings_metadata=None)
    print mdl.summary()
    print type(voxel_data)
    voxel_data=np.array(voxel_data)
    mdl.fit(voxel_data,
            y,
            epochs=epoch,
            batch_size=batch_size,
            shuffle=True,
            callbacks=[tfCallBack],
            verbose=2)

    # loss, acc = mdl.evaluate()
    # print("\n test loss: ", loss)
    # print("\n test accuracy: ", acc)
    # save the model
    if output == None:
        mdl.save('deepdrug3d.h5')
    else:
        mdl.save(output+'deepdrug3d.h5')


if __name__ == "__main__":
    args = myargs()
    train_deepdrug(args.pos_list, args.neg_list, args.vfolder, args.bs, args.lr, args.epoch, args.output)
