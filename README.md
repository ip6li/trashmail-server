# Trashmail Plugin

This is a Postfix plugin to receive trashmail mails by SMTP via Postfix and
save them into a MongoDB instance.

## Prerequisites

To take advantage of this plugin you need following components:

* A running Postfix installation, which is able to receive smtp mails
* Python 3.6 or later, with following modules:
** eml
** pymongo
* A MongoDB installation
* Optional: trashmail-client, so users are able to retrieve mails

## Installation

Create an user and group, e.g. *trashmail*, home directory can be */home/trashmail*.
Following examples presume home directory */home/trashmail*.

* Clone this project to  */home/trashmail*.
* Create a directory */home/trashmail/.trashmail*
* Create a config file */home/trashmail/.trashmail/lmtp-server.ini*
* Create a log config file */home/trashmail/.trashmail/logging.ini*

Contents of config files are explained in following sections.

## Postfix Configuration

You need to do some configuration for Postfix to set up this tool.
In main.cf you need following options:

### /etc/postfix/relay_domains

Set up transport trashmail for each domain which you want to use with that
plugin.

    example.com    trashmail
    example.net    trashmail

### /etc/postfix/main.cf

At least Postfix needs to be configured to use relay_domains, usage of a map
may be the best choice. Of course you may prefer other map type like ldap.

    relay_domains = btree:/etc/postfix/relay_domains
    transport_maps = btree:/etc/postfix/relay_domains
   
Feel free to use other Postfix mechanisms, there are no limitations regarding
other Postfix options.

### /etc/postfix/master.cf

To use transport trashmail it is necessary to define it in this file.

    trashmail   unix  -       n       n       -       -       pipe
      flags=FR user=trashmail argv=/home/trashmail/postfix-plugin/main.py
      ${client_address} ${client_hostname} ${sender} ${recipient}

You may select an other location for trashmail plugin, e.g. for use with Posfix
chroot option.

## Trashmail Config File

Config file is expected on location ~/.trashmail/lmtp-server.ini, format:

    [DEFAULT]
    mongo_url = mongodb://127.0.0.1:27017/
    mongo_db = trashmail-lmtp
    max_age = 60

mongo_url and mongo_db must match your MongoDB installation. Option max_age is used
for clean up process to remove messages older than max_age from MongoDB. Postfix
plugin does not care about this parameter.

## Logging Config Files

For syntax and options regarding logging see [2], following a small example:

```
[loggers]
keys=root,mail.log,internal_checks,lmtp,config,storage

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler
```

## MongoDB

It is recommended to use a Docker container for MongoDB. Due to
typical trashmail use cases, persistent storage is not necessary.

    docker run -d -p 27017:27017 -v ~/data:/data/db mongo

## Links

[1] [https://docs.python.org/3/library/logging.html] Python3 Logging module

[2] [https://docs.python.org/3/library/logging.config.html] Python3 Logging configuration module
