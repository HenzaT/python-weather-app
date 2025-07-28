## (In Progress) Python Weather App
This is a self-directed project. 

## Goals
For this project, I wanted to try out some Python by using Flask and connecting it to React for the front end. So far, I have had experience building full-stack applications using Rails and so wanted to try building the front and back end separately. 

## Tech Stack
- Flask (Python)
- Open Weather API
- Postman (to test requests)

## Process
I first set up my Flask project following the documentation: 

`mkdir python-weather-app`\
`cd python-weather-app`\
`python3 -m venv .venv`

Activate the virtual environment:

`. .venv/bin/activate`

Install Flask

`pip install Flask`

Create a new file in the project

`touch app.py`

I ensured any API keys would be stored safely by creating a .env file and installing 

`pip install python-dotenv`

This allowed me to safely fetch the API key from my .env file. 

When first connecting it to my react frontend, I came across an error regarding CORS. I discovered that CORS is a browser security feature, and without the CORS headers it would be impossible for the react frontend to make requests. 

## Reflections

## Future Additions
