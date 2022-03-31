# MailFriend

This project is designed to fetch - by POP3 - emails from a server,
parse its content(in a HTML table specific format) and export it's content to 
a JSON format.

It's JSON content will be available at an RESTful API server, 
to be able to be fetch by external programs.

## Setup and run

- To setup the project:

`$ source venv/bin/activate`

- To setup Flask:
- 
`$ export FLASK_APP=server.py`

- To execute mail fetch:

`$ python3 mail2.py`

- To execute REST server:

`$ flask run`

## Docker Building

- Build Image:

```$ docker image build -t  --no-cache flask_docker .```

- Run container:

```$ docker run -p 5000:5000 -d flask_docker ```

## Routes

- Calls GET path: `http://127.0.0.1:5000/calls?amount=n`, where `n` is the 
amount of emails to fetch.

