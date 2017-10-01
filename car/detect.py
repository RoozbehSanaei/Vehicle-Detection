# -*- coding: utf-8 -*-

import cv2

from car.desc import get_hog_features
from car.train import load_model
from car.scan import Slider


class ImgDetector(object):
    
    def __init__(self, classifier=load_model("model.pkl")):
        self._slider = None
        self._clf = classifier
        self.detect_boxes = []
    
    def run(self, image):
        """
        # Args
            image : ndarray, shape of (H, W, 3)
                BGR-ordered image
        
        # Returns
            drawed : ndarray, same size of image
                Image with patch recognized in input image        
        """
        self._slider = Slider(image)
        
        for patch in self._slider.generate_next():
            patch_gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
            
            # Todo : get_hog_features -> class
            feature_vector = get_hog_features([patch_gray])
            
            # predict_proba
            if self._clf.predict(feature_vector) == 1.0:
                self._set_detect_boxes()
        drawed = self._draw_boxes(image)
        return drawed

    def _set_detect_boxes(self):
        """Set detected box coordinate"""
        # Get current box coordinate & Draw
        p1, p2 = self._slider.get_bb()
        x1, y1 = p1
        x2, y2 = p2
        box = (x1, y1, x2, y2)
        self.detect_boxes.append(box)


    def _draw_boxes(self, image):
        """Draw detected boxes to an image"""
        
        clone = image.copy()
        for box in self.detect_boxes:
            p1 = (box[0], box[1])
            p2 = (box[2], box[3])
            cv2.rectangle(clone, p1, p2, (0, 255, 0), 2)
        return clone
        
        
        