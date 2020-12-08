import logging
from pathlib import Path

import PIL.Image as Image
from webapp.apps.furnitureClassifier.scripts.label_image import LabelImage


class ObjectExtractor():

    cur_path = str(Path(__file__).resolve().parent.parent.parent) + "/apps"
    file_save_path = "/furnitureClassifier/tf_files/test_files/"

    def get_objects(self, data):
        logging.info("Got a image: " + str(data.get("image")))
        image_data = data.get('image')
        response = self.get_labels_from_model(image_data=image_data)
        return {
            "image_name": str(image_data.name),
            "detected_objects": response}

    def get_labels_from_model(self, image_data):
        file_name = self.save_image(image_data)
        # result = LabelImage().label(file_name='/furnitureClassifier/tf_files/furniture_photos/test/sofa-1.jpg')
        result = LabelImage().label(file_name=str(file_name))
        return result

    def save_image(self, image_data):
        image = Image.open(image_data.file)
        image.save(self.cur_path + self.file_save_path + image_data.name)
        return self.file_save_path + image_data.name