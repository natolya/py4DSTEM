# Defines a class - DataCube - for storing / accessing / manipulating the 4D-STEM data

# For now, let's assume the data we're loading...
#  -is 3D data, with the real space dimensions flattened.
#  -does not have the scan shape stored in metadata
#
# Once we have other kinds of data, we can implement more complex loading functions which
# catch all the possibilities.


import hyperspy.api as hs
import numpy as np

class DataCube(Object):

    def __init__(self, filename):
        self.read_data(filename)
        self.set_scan_shape()

    def read_data(self,filename):
        #Load data
        try:
            hyperspy_file = hs.load(filename)
            self.raw_data = hyperspy_file.data
            self.metadata = hyperspy_file.metadata
            self.original_metadata = hyperspy_file.original_metadata
        except Exception as err:
            print("Failed to load", err)
            self.raw_data = np.random.rand(100,512,512)
        # Get shape of raw data
        if len(self.raw_data.shape)==3:
            self.R_N, self.Q_Ny, self.Q_Nx = self.raw_data.shape
            self.R_Nx, self.R_Ny = 1, self.R_N
        elif len(self.raw_data.shape)==4:
            self.R_Ny, self.R_Nx, self.Q_Ny, self.Q_Nx = self.raw_data.shape
            self.R_N = self.R_Ny*self.R_Nx
        else:
            print("Error: unexpected raw data shape of {}".format(self.raw_data.shape))

    def set_scan_shape(self,R_Ny,R_Nx):
        """
        Reshape the data give the real space scan shape.
        TODO: insert catch for 4D data being reshaped.  Presently only 3D data supported.
        """
        try:
            self.data4D = self.raw_data.reshape(R_Ny,R_Nx,self.Q_Ny,self.Q_Nx)
            self.R_Ny,self.R_Nx = R_Ny, R_Nx
        except ValueError:
            pass

    def set_diffraction_space_view(self,R_Ny,R_Nx):
        """
        Set the image in diffraction space
        """
        try:
            self.data4D = self.raw_data.reshape(R_Ny,R_Nx,self.Q_Ny,self.Q_Nx)
            self.R_Ny,self.R_Nx = R_Ny, R_Nx
        except ValueError:
            pass

