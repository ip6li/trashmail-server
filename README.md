# LMTP Server

This is a LMTP server for use with Postfix to receive trashmail mails by SMTP via Postfix and
save them into a MongoDB instance.

## Usage

    start src/main.py

This will listen on Port 10025 (default).

## Config file

Config file is expected on location ~/.trashmail/lmtp-server.ini, format:

    [DEFAULT]
    mongo_url = mongodb://127.0.0.1:27017/
    mongo_db = trashmail-lmtp
    max_age = 60
    lockfiledir = /tmp/lmtp-server
    bind = 127.0.0.1
    port = 10025

mongo_url and mongo_db must match client.

## Postfix Configuration

In main.cf you need following options:

    mailbox_transport = lmtp:inet:localhost:10025
    virtual_transport = lmtp:inet:localhost:10025

smtpd_recipient_restrictions should contain an entry:

    check_recipient_access pcre:/etc/postfix/recipient_access.pcr

Feel free to use other Postfix mechanisms like e.g.
relay_domains etc.

Create file /etc/postfix/recipient_access.pcre with following content:

    /(.+)/ prepend X-Original-To: $1

# MongoDB

It is recommended to use a Docker container for MongoDB. Due to
typical trashmail use cases, persistent storage is not necessary.

    docker run -d -p 27017:27017 -v ~/data:/data/db mongo

