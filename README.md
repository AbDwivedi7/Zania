# Zania

## Installation

This project requires Python 3.9 to run.

Activate virtual env.

Install the dependencies:
```sh
pip install -r requirements.txt 
```

Start the Server:
```sh
python manage.py runserver
```

## Authentication

This project uses JWT for authentication


## Endpoints

### Login

- URL    : http://127.0.0.1:8000/api/tokens/login
- METHOD : POST
- BODY   : {"username": "newton","password": "12345678"}

### Qna

- URL         : http://127.0.0.1:8000/api/qna/bot
- METHOD      : POST
- FORM DATA   : {"questions": filestream... ,"content": "filestream... }
- HEADER      : {"Authorization": "Bearer token"}


## Rate Limiting
For Anonymous User     : 100 Request per minute
For Authenticated User : 10 Request per minute


## License

MIT