# image-classification
An image classifier based on sensitive content categories (Adult content, Violent content, and Medical content). Utilizes Google Cloud Vision to classify images, and does preprocessing on images to convert them to base64 format. Also allows to preprocess URLs through webscraping, detecting all images on a website, and analyzing them.

## Run
To run the server, initiate the Flask back-end and the React front-end.

```
python ./back/app.py
cd front
npm run dev
```
React front-end uses Vite for startup. In order to start a production ready build, modifications have to be made for both Flask and React.