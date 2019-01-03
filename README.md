# LMTP Server

This is a LMTP server for use with Postfix to receive trashmail mails by SMTP via Postfix and
save them into a MongoDB instance.

## Usage

    start src/main.py

This will listen on Port 10025.

## Postfix Configuration

In main.cf you need following options:

    mailbox_transport = lmtp:inet:localhost:10025
    virtual_transport = lmtp:inet:localhost:10025

Feel free to use other Postfix mechanisms like e.g.
relay_domains etc.

# MongoDB

It is recommended to use a Docker container for MongoDB. Due to
typical trashmail use cases, persistent storage is not necessary.

    docker run -d -p 27017:27017 -v ~/data:/data/db mongo

