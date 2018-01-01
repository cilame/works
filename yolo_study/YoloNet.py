import keras
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dense, Input, BatchNormalization, LeakyReLU, Reshape
from keras.models import Sequential, Model

input_size = 448

input_image = Input(shape=(input_size, input_size, 3))

# Layer 1
x = Conv2D(16, (3,3), strides=(1,1), padding='same', name='conv_1', use_bias=False)(input_image)
x = BatchNormalization(name='norm_1')(x)
x = LeakyReLU(alpha=0.1)(x)
x = MaxPooling2D(pool_size=(2, 2))(x)

# Layer 2 - 5
for i in range(0,4):
    x = Conv2D(32*(2**i), (3,3), strides=(1,1), padding='same', name='conv_' + str(i+2), use_bias=False)(x)
    x = BatchNormalization(name='norm_' + str(i+2))(x)
    x = LeakyReLU(alpha=0.1)(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

# Layer 6
x = Conv2D(512, (3,3), strides=(1,1), padding='same', name='conv_6', use_bias=False)(x)
x = BatchNormalization(name='norm_6')(x)
x = LeakyReLU(alpha=0.1)(x)
x = MaxPooling2D(pool_size=(2, 2), strides=(1,1), padding='same')(x)

# Layer 7 - 8
for i in range(0,2):
    x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_' + str(i+7), use_bias=False)(x)
    x = BatchNormalization(name='norm_' + str(i+7))(x)
    x = LeakyReLU(alpha=0.1)(x)




temp_model = Model(input_image, x)
gridh,gridw = temp_model.get_output_shape_at(-1)[1:3]
output = Conv2D(7,(1,1), strides=(1,1), padding='same', name='conv_23', kernel_initializer='lecun_normal')(x)
output = Reshape((gridh,gridw,7))(output)
model = Model(input_image, output)
##input_image = Input(shape=(448, 448, 3))
##v = model(input_image)
##model2 = Model(input_image, v)


##
##shape=(90,90,3)
##
##model = Sequential()
##model.add(Conv2D(9,(3,3), padding="same", activation='relu', input_shape=shape))
##model.add(MaxPooling2D(2,2,padding="same"))
##model.add(Conv2D(9,(3,3), padding="same", activation='relu', input_shape=shape))
##model.add(MaxPooling2D(2,2,padding="same"))



##model.add(Flatten())
##model.add(Conv2D(1024,(23,23), padding="valid", activation='relu'))
##model.add(Conv2D(9,(3,3), padding="valid", activation='relu'))
##model.add(Dense(20, activation='relu'))



##model.add(Dense(classnum, activation='softmax'))
##
##
##
##model.compile('adam','categorical_crossentropy',metrics=['accuracy'])

##model = mkmodel(s.x.shape[1:],s.class_num)
##print 'train-------'
##model.fit(x,y,epochs=100)
##model.save('mytrain_model.h5')
##
##print '\ntrain_ok-------'
##loss,accuracy = model.evaluate(x,y)
##print 'loss:',loss
##print 'accuracy:',accuracy
