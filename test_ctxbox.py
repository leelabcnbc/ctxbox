import unittest
import scipy.io as sio
from ctxbox.io import savecx
import os.path
import numpy as np


# how to use it:
# put `sftp://raptor.cnbc.cmu.edu/opt/data/home/leelab/For_Summer/test.zip` inside test_data
# and expand it.


class MyTestCase(unittest.TestCase):
    def test_savecx_one_frame_legacy(self):
        # notes_mat = sio.loadmat('./test_data/test/notes.mat')['note']  # useless here.
        imgs_mat = sio.loadmat(os.path.join('test_data', 'test', 'imgs.mat'))['imgs']
        assert imgs_mat.shape == (1000, 1)
        for i in range(1000):
            img_data = imgs_mat[i, 0]
            with open(os.path.join('test_data', 'test', '{:05d}.ctx'.format(i + 1)), 'rb') as f:
                ctx_reference = f.read()
            # use legacy because Summer saved these files using dmns(4) = 1
            ctx_test = savecx(img_data, legacy=True)
            ctx_test_2 = savecx(img_data[np.newaxis, :, :], legacy=True)
            assert ctx_reference == ctx_test == ctx_test_2
            if (i + 1) % 100 == 0:
                print('{}/{} done'.format(i + 1, 1000))


if __name__ == '__main__':
    unittest.main()
