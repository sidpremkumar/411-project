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
            tone_input=string,
            content_type='text/plain'
        ).get_result()

        # Format results
        ret = []
        for tone in tone_analysis['document_tone']['tones']:
            ret.append(tone['tone_name'])

        for sentence in tone_analysis['sentences_tone']:
            for tone in sentence['tones']:
                ret.append(tone['tone_name'])

        # Return
        return ret


if __name__ == '__main__':
    # Main method for debugging only
    temp = StringAnalyser()
    print(temp.string_analysis("The Beagle should look like a miniature Foxhound, and is solid for the size. The Beagle’s moderate size enables the ability to follow on foot. Beagles can also be carried, and they can scurry around in thick underbrush. Their close hard coat protects them from underbrush. Their moderate build enables them to nimbly traverse rough terrain. The Beagle’s amiable personality allows this breed to get along with other dogs and to be a wonderful pet. Beagles are noted for their melodious bay. The deep muzzle allows more room for olfactory receptors, aiding the Beagle’s uncanny sense of smell."))
