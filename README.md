# Home lab

## Features

- [x] Basic server setup (Unattended upgrades / NTP)
- [ ] Firewall
- [x] LAN domain name resolution
- [x] CA for internal SSL certificates
- [x] Mounting SMB storage (Storage for Jellyfin / Paperless)
- [x] Jellyfin
    - [ ] Make accessible externally (nginx + letsencrypt somehow)
- [x] Paperless
- [x] Gitea
- [ ] Restic backup (Done manually, todo in ansible & auto-restore if possible)
- [ ] Wireguard ? (For safe remote access to internal network)

## Usage

### Becoming your own CA

Lets have HTTPs on everything ! As those will be local addresses, we won't use LetsEncrypt or anything like that, we will sign our own certificates.

Since adding domain per domain to each of your devices is a PITA, we'll create a CA certificate on you computer to store in a safe place, and generate certificates for everything you'll store on your network.

If you do not plan to have more than one domain (i.e. probably one machine, router.lan & *.router.lan) you can generate only one certificate through mkcert and you're good to go. That's not my case.

[How to create your CA certificates](/be-your-own-ca.md)


### Installing

Edit the inventories/hosts to fill with your details, then edit the `inventories/host_vars/router.yaml` to configure it as you wish.

No matter which option you choose for SSL, put your certificate for `{{hostname}}.{{tld}}` in files/{BASE_URL.crt,BASE_URL.key}

The machine on which it will be setup needs to have Debian 11 and a ssh server running and a user with password-less sudo permissions.

During debian setup, choose "ssh server" & "usual system tools"

Then simply run:
```
$ ansible-galaxy install -r requirements.yaml --force
$ ansible-galaxy collection install -r requirements.yaml --force
$ ansible-playbook -i inventories/hosts setup.yaml --ask-vault-pass
```

## Tested on

- Debian Bullseye (11) (x86_64 - In Virtualbox - During dev)
- Debian Bullseye (11) (x86_64 - Lenovo M75q)
- DietPi (ARM - Maybe, once the thing is working-ish I will try on it)
