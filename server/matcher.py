# Built-In Modules
from difflib import SequenceMatcher

# Local Modules
from string_analyzer import StringAnalyser
from image_analysis import ImageAnalyser


# Data about our dogs
# All data was taken from https://www.petfinder.com/dog-breeds/
DOG_TONES = {
    'Labrador': ['Joy', 'Analytical', 'Tentative', 'Tentative', 'Tentative', 'Analytical', 'Joy'],
    'Chihuahua': ['Tentative', 'Joy', 'Tentative'],
    'Golden Retriever': ['Tentative', 'Joy', 'Tentative'],
    'German Shepherd': ['Tentative', 'Joy', 'Tentative'],
    'Yorkshire Terrier': ['Confident', 'Confident', 'Confident'],
    'Poodle': ['Joy', 'Analytical', 'Joy', 'Analytical', 'Analytical', 'Tentative', 'Analytical', 'Joy'],
    'Beagle': ['Joy', 'Sadness', 'Tentative', 'Tentative', 'Sadness', 'Analytical', 'Joy', 'Analytical'],
}
DOG_IMAGES = {
    'Labrador': ['Labrador retriever dog', 'retriever dog', 'dog', 'domestic animal', 'animal',
                 'flat-coated retriever dog', 'coal black color'],
    'Chihuahua': ['Chihuahua dog', 'small dog', 'dog', 'domestic animal', 'animal',
                  'toy terrier dog', 'pink color'],
    'Golden Retriever': ['golden retriever dog', 'retriever dog', 'dog', 'domestic animal',
                        'animal', 'dachshund dog', 'light brown color'],
    'German Shepherd': ['field', 'nature', 'paddy', 'rice', 'grain', 'food product', 'food',
                        'athletic game', 'sport', 'Lawn', 'grass', 'herb', 'plant',
                        'Watering Hole', 'animal', 'dog', 'light brown color', 'reddish orange color'],
    'Yorkshire Terrier': ['Botanical Garden', 'nature', 'field', 'pasture', 'Yorkshire terrier dog',
                          'terrier dog', 'dog', 'domestic animal', 'animal', 'Formal Garden',
                          'chestnut color', 'pale yellow color'],
    'Poodle': ['standard poodle', 'poodle dog', 'dog', 'domestic animal', 'animal', 'large poodle', 'ash grey color'],
    'Beagle': ['beagle dog', 'hound dog', 'dog', 'domestic animal', 'animal', 'beagling (dog)', 'foxhound dog', 'English foxhound dog', 'greenishness color'],

}
LOCAL_DOG_IMAGES = {
    'Labrador': 'Labrador.png',
    'Chihuahua': 'Chihuahua.jpg',
    'Golden Retriever': 'GoldenRetriever.jpg',
    'German Shepherd': 'GermanShepherd.jpg',
    'Yorkshire Terrier': 'YorkshireTerrier.jpg',
    'Poodle': 'Poodle.jpg',
    'Beagle': 'Beagle.jpg'
}


class Matcher(object):
    """
    Matcher used to take user data and return dog
    """

    def match_data(self, data):
        """
        Helper function to clean tweets.

        :param Dict data: User data
        :return: Matched Dog
        :rtype: String
        """
        # Get our dogs
        dogs = DOG_IMAGES.keys()

        # Keep track of the dog with max similarity
        max_similarity = 0
        max_dog = None
        all_data = {}

        for dog in dogs:
            # Calculate image similarity
            image_similar = self.calculate_similarity(
                DOG_IMAGES[dog], data['image_analysis'])

            # Calculate tone similarity
            tone_similar = self.calculate_similarity(
                DOG_TONES[dog], data['twitter_analysis'])

            # If this beats our previous max, replace it
            sum_similarity = image_similar + tone_similar

            # Keep track of all data to return to the user
            all_data[dog] = int(sum_similarity)

            if sum_similarity > max_similarity:
                max_similarity = sum_similarity
                max_dog = dog

        # Return relevant data
        return (max_dog, max_similarity), all_data

    def calculate_similarity(self, list_a, list_b):
        """
        Helper function to calculate similarity between two lists

        :param List list_a: First list
        :param List list_b: Second list
        :return: Similarity
        :rtype: Int
        """
        # Keep track of total similarity
        total_similarity = 0

        # Loop over both lists matching each word against each other
        for word_a in list_a:
            for word_b in list_b:
                total_similarity += self.similar(word_a, word_b)

        # Return the final value
        return total_similarity

    def similar(self, a, b):
        """
        Helper function to find similarity between two strings a and b

        :param String a: First string
        :param String b: Second string
        :return: String similarity
        :rtype: Int
        """
        return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    # Main method for debugging only
    DATABASE_SCHEMA = {
        'username': None,
        'twitter_analysis': ['Sadness', 'Joy', 'Sadness', 'Tentative', 'Joy', 'Sadness', 'Sadness', 'Tentative', 'Analytical', 'Fear', 'Tentative', 'Joy', 'Confident', 'Analytical', 'Tentative', 'Analytical', 'Joy', 'Tentative', 'Joy', 'Tentative', 'Sadness', 'Sadness', 'Joy', 'Analytical', 'Analytical', 'Confident', 'Confident', 'Joy', 'Analytical', 'Tentative', 'Joy', 'Joy', 'Confident', 'Tentative', 'Joy', 'Joy', 'Joy', 'Joy', 'Analytical', 'Confident', 'Sadness', 'Joy', 'Sadness', 'Sadness', 'Analytical', 'Analytical', 'Joy', 'Confident', 'Joy', 'Joy', 'Analytical', 'Joy', 'Joy', 'Analytical', 'Confident', 'Joy', 'Joy'],
        'image_analysis': ['person', 'people', 'coal black color', 'ultramarine color'],
    }

    matcher = Matcher()
    import pdb; pdb.set_trace()
    matcher.match_data(DATABASE_SCHEMA)
