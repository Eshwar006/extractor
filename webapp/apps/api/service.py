import logging


class ObjectExtractor():

    def get_objects(self, data):
        logging.info("Got a image: " + str(data.get("image")))
        return {
            "image_name": str(data.get("image")),
            "detected_objecsts": [
            {"name": "Chair", "score": "92.2%"},
            {"name": "Sofa", "score": "22.5%"},
            {"name": "Shelf", "score": "6.7%%"},
            {"name": "Wardrobe", "score": "9.3%%"},
        ]}
