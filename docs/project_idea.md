# Project Ideas


## Idea 1: What type of dog are you?


  We want to develop a web application that will look at a picture of the user and their tweets in order to determine what type of dog you are. We will utilize (IBM Watson’s tone analyzer)[https://cloud.ibm.com/docs/services/tone-analyzer?topic=tone-analyzer-gettingStarted] in order to understand the user tweets and (Azures Vision API)[https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/] to extract tone from users face. We plan on comparing the results of those queries to set values pre-computed that relate to each type of dog breed. We will run the description of different dog breeds along with their images through our pipeline and save these hard-coded values to compare against users. Built on top of Flask, we will use a MongoDB database to store cached values and use Twitter OAuth in order to let users log in to get access to their tweets.

## Idea 2: What music do you want to listen today?


  We want to develop a web application that recommends music according to user’s preference and the weather of the day. We plan on gathering the weather information from 3rd party resource, and extract user’s music preference according to their playlists and history. We will store the category of music according to weather and collect data of user’s music preference for past few months.
