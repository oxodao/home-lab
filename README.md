# Home lab

## Features

- [x] Basic server setup (Unattended upgrades / NTP)
- [ ] Firewall
- [ ] Setup dnsmasq DHCP
- [x] LAN domain name resolution
- [x] CA for internal SSL certificates
- [x] Mounting SMB storage (Sonarr/radarr destination on a NAS)
- [ ] Jellyfin
- [ ] Torrent client
- [x] Sonarr / Radarr / Jackett
    - [ ] Torrent client link
    - [ ] Creating user accounts
    - [ ] Auto-linking to Jackett
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

You also need to create a file at that contains your samba password and add it to the smb_shares variable (Copy the dist file without the extension):
```
username=USERNAME
password=PASSWORD
domain=WORKGROUP
```

The machine on which it will be setup needs to have Debian 11 and a ssh server running and a user with password-less sudo permissions.

Then simply run:
```
$ ansible-galaxy install -r requirements.yaml --force
$ ansible-galaxy collection install -r requirements.yaml --force
$ ansible-playbook -i inventories/hosts setup.yaml --ask-vault-pass
```

## Tested on

- Debian Bullseye (11) (x86_64 - In Virtualbox - During dev)
- DietPi (ARM - Maybe, once the thing is working-ish I will try on it)
