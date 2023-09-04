# ChatWithPDF

# Google Palm 2 API Integration

This repository contains code for integrating the Google Palm 2 API into your project. In order to use this API, you will need to obtain a Google API key and store it in a `.env` file. This README will guide you through the process.

## Prerequisites

Before you can use the Google Palm 2 API, make sure you have the following:

1. **Google API Key**: You must obtain an API key from Google's Developer Console. Follow the steps below to obtain one.

## Obtaining a Google API Key
Visit https://developers.generativeai.google/products/palm

## Setting up the `.env` File

To securely store your API key, create a `.env` file in the root of your project directory if it doesn't already exist. Add the following content to the `.env` file:

```
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Replace `YOUR_API_KEY_HERE` with the API key you obtained from the Google Developer Console.

## To run the app

Step 1:
```
pip install -q -r requirements.txt
```

Step 2:
```
streamlit run app.py
```
