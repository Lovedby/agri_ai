# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import numpy as np
from six.moves import xrange
import random

'''
DON'T CHANGE.
'''
VALIDATION_START = 10
VALIDATTION_END = 13
TIME_STEP = 24

class DataSets(object):

    '''
    @param train_path: Path of train dataset csv file. 
    @param test_path: Path of test dataset csv file.
    '''

    def __init__(self, train_path, test_path):

        all_data=[]
        train_index = []
        validation_index = []

        train_data, train_indexes, validation_indexes = self._read_file(train_path)
        test_data, test_indexes, _ = self._read_file(test_path, False)


        self.train_data = np.array(train_data)
        self.test_data = np.array(test_data)
        self.train_indexes = train_indexes
        self.validation_indexes = validation_indexes
        self.test_indexes = test_indexes
        print("train:%d,validation:%d,test:%d"%(len(self.train_indexes,),len(self.validation_indexes),len(self.test_indexes)))

        self.average = np.mean(self.train_data, axis=0, keepdims=True)
        self.std = np.std(self.train_data, axis=0, keepdims=True)
        self.max = np.max(self.train_data, axis=0, keepdims=True)
        self.min = np.min(self.train_data, axis=0, keepdims=True)

        self.stand_train_data = (self.train_data - self.average)/self.std
        self.stand_test_data = (self.test_data - self.average)/self.std

        self.validation_data = self._create_batch(self.validation_indexes)
        self.test_data = self._create_batch(self.test_indexes, True)

    def _read_file(self, file_path, train=True):

        all_data =[]
        input_indexes=[]
        v_input_indexes=[]

        num_line = 0

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                float_row = row[5:]
                float_row = [float(elem) for elem in float_row]
                all_data.append(float_row)

                if row[4] == str(1):
                    if train and int(row[2]) >= VALIDATION_START and int(row[2]) <= VALIDATTION_END:
                        v_input_indexes.append(num_line)
                    else:
                        input_indexes.append(num_line)
                num_line += 1

        return all_data, input_indexes, v_input_indexes


    def _create_batch(self, indexes, test=False, batch_size=None):

        target = indexes
        if batch_size:
            target = random.sample(target, batch_size)
        input_batch = []
        correct_batch = []

        for index in target:
            input_time_step = []
            correct_time_step = []
            for i in xrange(TIME_STEP):
                if test:
                    input_time_step.append(self.stand_test_data[index+1])
                    correct_time_step.append(self.stand_test_data[index+TIME_STEP+i])
                else:
                    input_time_step.append(self.stand_train_data[index+1])
                    correct_time_step.append(self.stand_train_data[index+TIME_STEP+i])

            input_batch.append(input_time_step)
            correct_batch.append(correct_time_step)
        return (np.array(input_batch), np.array(correct_batch))
         
    '''
    @param batch_size: Num of batch size.
    '''
    def get_next_batch(self, batch_size):
        input_batch , correct_batch = self._create_batch(self.train_indexes, batch_size=batch_size)
        return (input_batch, correct_batch)






        