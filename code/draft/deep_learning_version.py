'''
가위 바위 보 인식 모델 중
첫번째, keras 모델을 이용한 모델
'''


from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Load the model
model = load_model('data\keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
image = Image.open('<IMAGE_PATH>')
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)


image_array = np.asarray(image)
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
print(prediction)
