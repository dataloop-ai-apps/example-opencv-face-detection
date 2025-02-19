import dtlpy as dl
import logging
import cv2

logger = logging.getLogger('face-detector')


import dtlpy as dl
import logging
import cv2

logger = logging.getLogger('face-detector')


class ServiceRunner(dl.BaseServiceRunner):
    def __init__(self):
        # Initialize the face detection model
        self.model = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def predict(self, item: dl.Item) -> dl.Item:
        try:
            # Download the image as an array
            image = item.download(save_locally=False, to_array=True)
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            logger.info(f'Running face detection on item: {item.id}')
            
            # Detect faces in the image
            faces = self.model.detectMultiScale(gray, 1.1, 4)
            logger.info(f'Found {len(faces)} faces.')
            
            # Create an annotation collection
            image_annotations = dl.AnnotationCollection()
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    image_annotations.add(annotation_definition=dl.Box(left=float(x),
                                                                      top=float(y),
                                                                      right=float(x + w),
                                                                      bottom=float(y + h),
                                                                      label='face'),
                                          model_info={'name': 'haarcascade_frontalface_default',
                                                      'model_id': 'haarcascade_frontalface_default',
                                                      'confidence': 1})
            # Upload annotations to the item
            item.annotations.upload(image_annotations)
        except Exception as e:
            logger.error(f'Error processing item {item.id}: {str(e)}')
            raise
        return item