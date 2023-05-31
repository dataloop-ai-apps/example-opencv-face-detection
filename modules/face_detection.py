import dtlpy as dl
import logging
import cv2

logger = logging.getLogger('face-detector')

face_detector = dl.AppModule('face-detector', description='OpenCV model for face detection')

# we can load the model here
model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# or set init function to load at startup
@face_detector.set_init()
def load_models():
    logger.info('loading a model in the init function')
    face_detector.model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    logger.info(f'model in loaded')


@face_detector.add_function()
def predict(item: dl.Item) -> dl.Item:
    image = item.download(save_locally=False, to_array=True)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    logger.info(f'running face detection on item: {item.id}')
    faces = face_detector.model.detectMultiScale(gray, 1.1, 4)
    logger.info(f'found {len(faces)} faces')
    image_annotations = dl.AnnotationCollection()
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            print(f'{x}, {y}, {x + h}, {y + w}')
            image_annotations.add(annotation_definition=dl.Box(left=float(x),
                                                               top=float(y),
                                                               right=float(x + w),
                                                               bottom=float(y + h),
                                                               label='face'),
                                  model_info={'name': 'haarcascade_frontalface_default',
                                              'confidence': 1})
    item.annotations.upload(image_annotations)
    return item


if __name__ == "__main__":
    item = dl.items.get(item_id='642d26bf822c85d699e57551')
    face_detector.init()
    face_detector.predict(item=item)
    print(face_detector.to_json())
