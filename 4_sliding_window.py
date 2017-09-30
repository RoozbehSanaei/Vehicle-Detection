# -*- coding: utf-8 -*-

import cv2


class ImgScanner(object):
    
    def __init__(self):
        pass

    def get_patch(self):
        pass

class ImgPyramid(object):
    
    def __init__(self):
        pass
    
    def get_image(self):
        pass


class ImageScanner(object):
    """This class provides image scanning interfaces of sliding window concept."""
    
    def __init__(self, image):
        self._layer = image
        self._bounding_box = None
        self.scale_for_original = 1.0
    
    def get_next_patch(self, step_y=10, step_x=10, win_y=30, win_x=30):
        
        for y in range(0, self._layer.shape[0] - win_y, step_y):
            for x in range(0, self._layer.shape[1] - win_x, step_x):
                self._bounding_box = self._get_bb(y, y+win_y, x, x+win_x)
                yield (y, x, self._layer[y:y + win_y, x:x + win_x])
    
    def get_next_layer(self, scale=0.7, min_y=30, min_x=30):
        yield self._layer

        while True:
            h = int(self._layer.shape[0] * scale)
            w = int(self._layer.shape[1] * scale)
            
            self._layer = cv2.resize(self._layer, (w, h))
            
            if h < min_y or w < min_x:
                break
            self.scale_for_original = self.scale_for_original * scale
            yield self._layer

    @property
    def bounding_box(self):
        if self._bounding_box is None:
            raise ValueError('bounding box does not defined.')
        else:
            return self._bounding_box

    def _get_bb(self, y1, y2, x1, x2):
        """Get bounding box in the original input image"""
        original_coords = [int(c / self.scale_for_original) for c in (y1, y2, x1, x2)]
        return original_coords

    
if __name__ == "__main__":
    import time
    
    image = cv2.imread("test_images//test1.jpg")
    image_scanner = ImageScanner(image[200:400, 200:400, :])
    
    for layer in image_scanner.get_next_layer():
        for y, x, window in image_scanner.get_next_patch():
            clone = layer.copy()
            cv2.rectangle(clone, (x, y), (x + 30, y + 30), (0, 255, 0), 2)
            cv2.imshow("Test Image Scanner", clone)
            cv2.waitKey(1)
            time.sleep(0.025)
            
    
    
    