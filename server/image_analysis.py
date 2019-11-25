# Build in Modules
import os

# 3rd Party Modules
from ibm_watson import VisualRecognitionV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Local Modules
from string_analyzer import StringAnalyser


# Global Variables
authenticator = IAMAuthenticator(os.environ['VISUAL_API'])
visual_recognition = VisualRecognitionV3(
    version='2016-05-20',
    authenticator=authenticator
)
string_analyzer = StringAnalyser()

class ImageAnalyser(object):
    """
    Object to do our image analysis
    """

    def __init__(self):
        pass

    def analyse(self, image_url):
        """
        Our analyze function
        :param String image_url: URL of the image
        :return: Image tones
        :rtype: List
        """
        # Try to classify our image_url
        try:
            response = visual_recognition.classify(url=image_url)
        except ApiException:
            print(f"DEBUG: ImageAnalyser: {image_url} returned an error.")
            return None

        # Parse the results
        classifications = response.result['images'][0]['classifiers'][0]['classes']

        # Loop over our classifications and add to a final string
        final_classes = []
        for classification in classifications:
            new_class = classification['class']
            final_classes.append(new_class)

        # Return our tones
        return final_classes


if __name__ == '__main__':
    # Main method for debugging only
    temp = ImageAnalyser()
    temp.analyse(
        'https://watson-developer-cloud.github.io/doc-tutorial-downloads/visual-recognition/visual-recognition-food-fruit.png')