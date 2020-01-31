## React Setup

 ```
 cd client
 ```

 ```
 npm install
 ```

## Start React (inside client folder)
` node start `

## Flask Setup

Make sure you have virtualenv installed, gonna assume you are on a Windows platform

`py -m pip install --user virtualenv

Navigate to the project folder, and activate virtualenv
by typing the following into the command prompt

`.\env\Scripts\activate`

Install everything by doing

`py -m pip install -r requirements.txt`

If you added more dependencies then do
`py -m pip freeze > requirements.txt`

while you are still in your virtual environment

### Don't forget to add your API keys to app.py

### Callback URL is: http://127.0.0.1:8080/callback/twitter

## Start Server
`python app.py`

depending on your configuration you might have to say python3 instead
