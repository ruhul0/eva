#%% Setup.
import numpy as np

from keras.datasets import cifar10, mnist
from keras.utils.visualize_util import plot
from keras.callbacks import TensorBoard, ModelCheckpoint

from eva.models.pixelcnn import PixelCNN
from eva.models.gated_pixelcnn import GatedPixelCNN

from eva.util.mutil import clean_data

#%% Data.
DATASET = mnist

DATA, LABELS = clean_data(DATASET.load_data(), rgb=True, latent=False)

#%% Model.
MODEL = GatedPixelCNN
FILTERS = 126
BLOCKS = 1

ARGS = (DATA.shape[1:], FILTERS, BLOCKS)
if MODEL == GatedPixelCNN and LABELS is not None:
    ARGS += (1,)

M = MODEL(*ARGS)

M.summary()

plot(M)

#%% Train.
M.fit(DATA if LABELS is None else [DATA, LABELS],
      [(np.expand_dims(DATA[:, :, :, c].reshape(DATA.shape[0], DATA.shape[1]*DATA.shape[2]), -1)*255).astype(int) for c in range(DATA.shape[3])],
      batch_size=32, nb_epoch=200,
      verbose=1, callbacks=[TensorBoard(), ModelCheckpoint('model.h5', save_weights_only=True)]) # Only weights because Keras is a bitch.