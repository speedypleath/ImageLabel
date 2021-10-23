import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/hdd/memory-box-329820-6a22d487571d.json"
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('a-man-walking-in-the-street-with-his-dog.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)