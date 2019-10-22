# Built in Modules
import os

# 3rd Party Modules
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import nltk


# Global Variables
# IBM Watson Tone Analyzer:
authenticator = IAMAuthenticator(os.environ['IAM_APIKEY'])
CONFIG = ToneAnalyzerV3(
    version="2017-09-21",
    authenticator=authenticator,
)

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

class StringAnalyser(object):
    """
    Object to represent the IBM watson tone analyzer
    """

    def __init__(self):
        pass

    def string_analysis(self, string):
        """
        Function to analyse a string
        :param String string: String to analysis
        :return:
        """
        # Call the API
        tone_analysis = CONFIG.tone(
            {'text': string},
            content_type='application/json'
        ).get_result()

        # Format results
        ret = []
        for tone in tone_analysis['document_tone']['tones']:
            ret.append(tone['tone_name'])

        # Return
        return ret


if __name__ == '__main__':
    # Main method for debugging only
    temp = StringAnalyser()
    temp.string_analysis("test")