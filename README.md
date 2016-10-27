# nfsn-tls
Automatically enable and/or update TLS on NearlyFreeSpeech.net sites using Dehydrated (an unofficial Let's Encrypt tool)

## Usage

### Synopsis

    tls (--install | --update) [-fqh] DOMAIN

### Positional argument

Argument | Description
-------- | -----------
`DOMAIN` | Your bare domain name (`example.com`, not `www.example.com`).

**IMPORTANT NOTE:** This script *DOES NOT* work with NFSN default names, such as `example.nfshost.com`.

### Required arguments

One (and only one) of the following arguments is required:

Required Argument | Description
-------- | -----------
`--install` | Enable Let's Encrypt for the first time
`--update` | Update your certificate, if necessary. Will not update certificates which are valid for at least two more weeks unless `-f`/`--force` is given.

### Optional arguments

Optional Argument | Description
-------- | -----------
`-f`, `--force` | With `--update`, force certificate update even if it is not necessary
`-q`, `--quiet` | With `--update`, exit silently if no update is carried out. Useful to avoid useless messages from `cron`.
`-h`, `--help` | Show this help message and exit
