import keras
from keras.layers import Dense, Conv2D, MaxPooling2D, Activation, Flatten, Dense
from keras.models import Sequential

from CreateCate import CreateCate
s = CreateCate('pictt1','pictt2')
s.save_mapdict('my_mapdict.pickle')
x = s.x/255
y = s.y


model = Sequential()
model.add(Conv2D(32,(3,3), padding="same", activation='relu', input_shape=(160,210,3)))
model.add(MaxPooling2D(2,2,padding="same"))
model.add(Conv2D(64,(3,3), padding="same", activation='relu'))
model.add(MaxPooling2D(2,2,padding="same"))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(len(y[0]), activation='softmax'))

model.compile('adam','categorical_crossentropy',metrics=['accuracy'])
print 'train-------'
model.fit(x,y,epochs=16)
model.save('my_model2.h5')

print '\ntrain_ok-------'
loss,accuracy = model.evaluate(x,y)
print 'loss:',loss
print 'accuracy:',accuracy
