"""Required Imports"""

import os
import random
import matplotlib
import numpy as np
from scipy import ndimage
import zipfile
from pathlib import Path
#from PIL import Image

FILE_NAME = 'conformers'
FILE_ITER_NAME = 'conformer'
DATA_DIR = 'data/json/'
HEADER_LENGTH = 6
NUM_CHANNELS = 3

def valExtract(line, str):
    strline = line.decode("utf-8")
    if(strline.find(str) != -1):
        for s in strline.split():
            if (str != 'electrons'):
                if(s[:-1].isdigit()):
                    return s[:-1]
            else:
                if(s.isdigit()):
                    return s
    return -1

def generateVis(outfile, index, numVoxels, x, y, z, protons, neutrons, electrons):
    if (index != -1):
        filename = outfile + str(index) + '.xyz'
    else:
        filename = outfile + '.xyz'

    if (not os.path.isfile(filename)):
        f = open(filename, 'w')
        f.write(str(numVoxels)+'\n\n')
    else:
        f = open(filename, 'a')

    if (protons):
        eName = 'O'
    else:
        eName = 'H'
    f.write(eName + ' ' + str(x) + ' ' + str(y) + ' ' + str(z)+'\n')
    f.close()

def extractTrainingData(dir, filename, file_iter_name, index = 0, vis = True):
    archive = zipfile.ZipFile(os.path.join(dir, FILE_NAME+'.zip'), 'r')
    if (index == -1):
        file = file_iter_name+'.json'
    else:
        file = file_iter_name + str(index) + '.json'

    jsonFile = archive.open(file, 'r')
    numVoxels = int((len(jsonFile.readlines())-6)/8)
    jsonFile = archive.open(file, 'r')

    jsonFile = archive.open(file, 'r')
    jsonFile.readline()
    gridDimensions = int(jsonFile.readline().split()[2])

    voxelGrid = np.zeros((gridDimensions, gridDimensions, gridDimensions, NUM_CHANNELS))

    for i in range(0, HEADER_LENGTH-4):
        jsonFile.readline()

    bindingEnergy = float(jsonFile.readline().split()[2])

    for i in range(0, numVoxels):
        jsonFile.readline()
        jsonFile.readline()
        xpos, ypos, zpos = int(jsonFile.readline().split()[1][:-1]), int(jsonFile.readline().split()[1][:-1]), int(jsonFile.readline().split()[1][:-1])
        protons, neutrons, electrons = int(jsonFile.readline().split()[1][:-1]), int(jsonFile.readline().split()[1][:-1]), int(jsonFile.readline().split()[1])
        if (vis):
            generateVis(file_iter_name, index, numVoxels, xpos, ypos, zpos, protons, neutrons, electrons)
        voxelGrid[xpos, ypos, zpos, 0], voxelGrid[xpos, ypos, zpos, 1], voxelGrid[xpos, ypos, zpos, 2] = protons, neutrons, electrons
    print(index)

    return voxelGrid

for i in range(1,12):
    extractTrainingData(DATA_DIR, FILE_NAME, FILE_ITER_NAME, index=i)
