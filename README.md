# moleCare - CNN project

[moleCare](http://fjos1.herokuapp.com/) is an application that uses Convolutional Neural Networks (CNN) to classify images of skin moles as malignant or benign. 

## Some highlights:

- We applied transfer learning and used the pre-trained MobileNet v2 model to train our data. Additional layers were added to fine tune our model.
- The API was developed with [Flask framework](https://flask.palletsprojects.com/en/1.1.x/). 
- The application was built in a Docker, and the resulting Docker image was then deployed to Heroku.
