import tensorflow as tf
import numpy as np

weight_decay = 0.0005
learning_rate = 0.0001

inputs = tf.keras.layers.Input(shape=(384, 256, 1))
x = tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(inputs)
x = tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.MaxPooling2D(pool_size=(4, 4), strides=2, padding='same')(x)

x = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.MaxPooling2D(pool_size=(4, 4), strides=2, padding='same')(x)

x = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(256, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.MaxPooling2D(pool_size=(4, 4), strides=2, padding='same')(x)

x = tf.keras.layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x_0 = tf.keras.layers.Conv2D(512, kernel_size=(3, 3), activation='relu', padding='same',
                             kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x_1 = tf.keras.layers.Conv2D(21, kernel_size=(1, 1), padding='same',
                             kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x_0)
x = tf.keras.layers.concatenate([x_0, x_1])

x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x_2 = tf.keras.layers.Conv2D(21, kernel_size=(1, 1), padding='same',
                             kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.concatenate([x_0, x_1, x_2])

x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(7, 7), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(21, kernel_size=(1, 1), padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(32, kernel_size=(3, 3), strides=2, activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(64, kernel_size=(3, 3), strides=2, activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)
x = tf.keras.layers.Conv2D(128, kernel_size=(3, 3), strides=2, activation='relu', padding='same',
                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))(x)

x = tf.keras.layers.Flatten()(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.Dropout(0.2)(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.Dropout(0.2)(x)
x = tf.keras.layers.Dense(63)(x)

adam = tf.keras.optimizers.Adam(lr=learning_rate)
model = tf.keras.models.Model(inputs=inputs, outputs=x)
model.compile(loss='mean_squared_error', optimizer=adam, metrics=['accuracy'])
model.summary()

inputs = np.load("inputs.np")
outputs = np.load("outputs.np")
train_x = inputs[:70000]
train_y = outputs[:70000]
valid_x = inputs[70000:72000]
valid_y = outputs[70000:72000]
test_x = inputs[72000:]
test_y = outputs[72000:]
epochs_num = 150

checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath='./saved_model/weights.{epoch:02d}-{loss:.4f}.hdf5',
                                                save_best_only=False, save_weights_only=False)
history = model.fit(train_x, train_y,
                    epochs=epochs_num, validation_data=(valid_x, valid_y), batch_size=8,
                    callbacks=[checkpoint], verbose=1)
