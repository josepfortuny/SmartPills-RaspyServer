# Importing the Keras libraries and packages
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import random
import os
import numpy as np
import matplotlib.pyplot as plt


"""
Class that implements the Neural network
"""
class NeuralNetwork():
    IMG_HEIGHT = 64
    IMG_WIDTH = 64
    def __init__(self,path):
        self.path = path


    def init_training_neural_network(self):
        """
        batch normalization
        Normalizing the input or output of the activation functions in a hidden layer. Batch normalization can provide the following benefits:

        Make neural networks more stable by protecting against outlier weights.
        Enable higher learning rates.
        Reduce overfitting.
        """
        self.batch_size = 128
        # num, generations
        self.epoch = 15
        # directories with our training & Validation pictures
        self.train_dir = os.path.join(self.path,'train')
        self.train_bluePill_dir = os.path.join(self.train_dir, 'metadol')
        self.train_redPill_dir = os.path.join(self.train_dir, 'metaspirina')
        self.validation_dir = os.path.join(self.path, 'validation')
        self.validation_bluePill_dir = os.path.join(self.validation_dir, 'metadol')
        self.validation_redPill_dir = os.path.join(self.validation_dir, 'metaspirina')
        self.total_validation = len(os.listdir(self.validation_bluePill_dir)) + len(os.listdir(self.validation_redPill_dir))
        self.total_training = len(os.listdir(self.train_bluePill_dir)) + len(os.listdir(self.train_redPill_dir))
    def is_trained(self):
        return os.path.isfile('/home/pi/mu_code/theModel.h5')

    def how_many_images(self):
        # lets look how many cats and dogs images are in the training validaton directori

        print('total training bluePill images:', len(os.listdir(self.train_bluePill_dir)))
        print('total training redPill images:', len(os.listdir(self.train_redPill_dir)))
        print('total training bluePill images:', len(os.listdir(self.train_bluePill_dir)))
        print('total training redPill images:', len(os.listdir(self.train_redPill_dir)))
    def predict_image(self):
        test_path = self.path + 'test/test' + str(random.randrange(10)) + '.jpg'

        #plt.imshow(self.test_path)
        #img = Image.open(self.test_path)
        #img.show()
        #prova =/home/pi/Desktop/Grupo08/neuralnetwork/datasets/test/test.jpg
        os.system("gpicview " + test_path)
        test_image = image.load_img((test_path),target_size = (self.IMG_HEIGHT,self.IMG_WIDTH))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        classifier = load_model('theModel.h5')
        result = classifier.predict(test_image)
        #training_set.class_indices
        #print ("reuslt" , result[0][0])
        if result[0][0] >= 0.5:
            print('Pill predicted is : RedPill')
            return "RedPill"

        else:
            print('Pill predicted is : BluePill')
            return "BluePill"

    def train_neural_network(self):
        self.init_training_neural_network()
        """  Data Preparation
        Format the images into appropriately pre-processed
        floating point tensors before feeding to the network:

         1. Read images from the disk.

         2. Decode contents of these images and convert it into
            proper grid format as per their RGB content.

         3. Convert them into floating point tensors.

         4. Rescale the tensors from values between 0 and 255 to values between 0 and 1,
            as neural networks prefer to deal with small input values.

        Fortunately, all these tasks can be done with the ImageDataGenerator class provided by tf.keras.
        It can read images from disk and preprocess them into proper tensors.
        It will also set up generators that convert these images into batches of tensors—helpful when training the network.
        """
        # Generator for our training data
        train_image_generator = ImageDataGenerator(rescale=1./255)
        validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

        """
        After defining the generators for training and validation images,
        the flow_from_directory method load images from the disk, applies rescaling,
        and resizes the images into the required dimensions.
        """
        train_data_gen = train_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                   directory=self.train_dir,
                                                                   shuffle=True,
                                                                   target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                   class_mode='binary')
        val_data_gen = validation_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                      directory=self.validation_dir,
                                                                      target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                      class_mode='binary')
        """ Create the model
        The model consists of three convolution blocks with a max pool layer in each of them.
        There's a fully connected layer with 512 units on top of it that is activated by a relu activation function.

        """
        model = Sequential([
            Conv2D(16, 3, padding='same', activation='relu', input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH ,3)),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(1, activation = 'sigmoid')
        ])
        """
        Compile the model
        For this tutorial, choose the ADAM optimizer and binary cross entropy loss function.
        To view training and validation accuracy for each training epoch, pass the metrics argument.
        """
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        """
        Model summary
        View all the layers of the network using the model's summary method:
        """
        model.summary()
        """
        Train the model
        se the fit_generator method of the ImageDataGenerator class to train the network.
        """
        history = model.fit_generator(
        train_data_gen,
        steps_per_epoch=self.total_training ,
        epochs=self.epoch,
        validation_data=val_data_gen,
        validation_steps=self.total_validation
        )
        """save a Keras model into a single HDF5 file which will contain:

        the architecture of the model, allowing to re-create the model
        the weights of the model
        the training configuration (loss, optimizer)
        the state of the optimizer, allowing to resume training exactly where you left off."""
        model.save('theModel.h5')