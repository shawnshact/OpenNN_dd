import numpy as np

#used to check if float
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#parses json file for molecule space
def parser(filepath):

    file = open(filepath, "r") #open molecule space filepath

    #extract header information
    file.readline()
    gridDimensions = int(file.readline().split()[2])
    voxelSize = float(file.readline().split()[2])
    transforms = [float(s) for s in file.readline().split() if is_float(s)]
    bindingEnergy = float(file.readline().split()[2])
    file.readline()

    #allocate 4D matrix then populate... 3 channels, protons, neutrons, electrons
    grid = np.zeros((gridDimensions, gridDimensions, gridDimensions, 3), dtype = int)
    for i in range(0,gridDimensions):
        for j in range(0,gridDimensions):
            for k in range(0,gridDimensions):
                file.readline() #get rid of {
                grid[i][j][k][0] = int(file.readline().split()[1].split(',')[0])
                grid[i][j][k][1] = int(file.readline().split()[1].split(',')[0])
                grid[i][j][k][2] = int(file.readline().split()[1])
                file.readline() #get rid of },

    #close file and return
    file.close()
    return grid
