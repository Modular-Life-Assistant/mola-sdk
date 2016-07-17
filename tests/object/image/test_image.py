import os
import resource
import unittest
from io import BytesIO

from mola_sdk.object.Image import Image

try:
    from PIL import Image as ImagePil  # Pillow
except:
    import Image as ImagePil


class CronTestCase(unittest.TestCase):
    def setUp(self):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.img_path = os.path.join(current_dir_path, 'test.jpg')

    def test_cast(self):
        """cast image check"""
        img = Image(path=self.img_path)
        cast_img = Image(path=self.img_path)

        cast_img = Image(opencv_image=cast_img.get_opencv())
        self.assertEqual(img, cast_img, 'img to opencv')

        cast_img = Image(pil_image=cast_img.get_pil())
        self.assertEqual(img, cast_img, 'img to pil')

    def test_diff_percent(self):
        """different_percent method check"""
        img = img1 = Image(path=self.img_path)

        self.assertEqual(img1.diff_percent(img1), 0)
        self.assertEqual(img, img1)

        img2 = Image(path=self.img_path).greyscale()

        self.assertEqual(img.diff_percent(img2), 100)
        self.assertNotEqual(img, img2)

    def test_empty_parameter(self):
        """Empty parameter test"""
        with self.assertRaises(AttributeError) as context:
            Image()

        self.assertEqual(
            'pil_image or opencv_image or raw or path is required',
            str(context.exception)
        )

    def test_from_opencv(self):
        """load image from OpenCV object check"""
        import cv2
        img1 = Image(path=self.img_path)
        img2 = Image(opencv_image=cv2.imread(self.img_path))
        self.assertEqual(img1.diff_percent(img2), 0)
        self.assertEqual(img1, img2)

    def test_from_pil(self):
        """load image from PIL object check"""
        with open(self.img_path, 'rb') as f:
            raw = f.read()

        pil_image = ImagePil.open(BytesIO(raw))
        img1 = Image(pil_image=pil_image)
        img2 = Image(path=self.img_path)
        self.assertEqual(img1.diff_percent(img2), 0)
        self.assertEqual(img1, img2)

    def test_from_row(self):
        """load image from raw string check"""
        with open(self.img_path, 'rb') as f:
            raw = f.read()

        img1 = Image(path=self.img_path)
        img2 = Image(raw=raw)
        self.assertEqual(img1.diff_percent(img2), 0)
        self.assertEqual(img1, img2)

    def test_save(self):
        """save image check"""
        path_save = '/tmp/MoLA_test/test.jpg'

        img = Image(path=self.img_path)
        img.save(path_save, quality=100)

        self.assertEqual(Image(path=path_save), img)
