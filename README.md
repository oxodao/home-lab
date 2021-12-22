# Home Router

## Features

- [ ] Setup PiHole or something similar
- [ ] LAN domain name resolution
- [x] CA for internal SSL certificates
- [ ] Jellyfin
- [ ] Torrent client
- [x] Sonarr / Radarr (Still misses torrent client link + creating user account)

## Usage

### Installing dependencies
```
$ ansible-galaxy install -r requirements.yaml --force
$ ansible-galaxy collection install community.docker
$ ansible-galaxy collection install community.crypto
```

### Becoming your own CA

Lets have HTTPs on everything ! As those will be local addresses, we won't use LetsEncrypt or anything like that, we will sign our own certificates.

Since adding domain per domain to each of your devices is a PITA, we'll create a CA certificate on you computer to store in a safe place, and generate certificates for everything you'll store on your network.

If you do not plan to have more than one domain (i.e. probably one machine, router.lan & *.router.lan) you can generate only one certificate through mkcert and you're good to go. That's not my case.

[How to create your CA certificates](/be-your-own-ca.md)

No matter which option you choose, put your certificate in files/{BASE_URL.crt,BASE_URL.key}

### Installing

The machine on which it will be setup needs to have Debian 11 and a ssh server running.

The user needs to have passwordless sudo perms

## Tested on

- Debian Bullseye (11) (x86_64 - In Virtualbox - During dev)
- DietPi (ARM - Maybe, once the thing is working-ish I will try on it)
