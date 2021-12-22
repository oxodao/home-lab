# Become your own CA (Archlinux cert-trusting only)

__Stolen from [deliciousbrains.com](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)__

## Generating root certs
### Private key
```
$ openssl genrsa -des3 -out oxo-ca.key 2048
```

### Root certificate
```
$ openssl req -x509 -new -nodes -key oxo-ca.key -sha256 -days 1825 -out oxo-ca.pem
```

### Convert the root certificate to crt

If needed only
```
$ openssl x509 -outform der -in oxo-ca.pem -out oxo-ca.crt
```

## Installing the root certificate
### NSS

Chromium, Firefox, Thunderbird, Evolution, SeaMonkey use NSS for retrieving trusted CAs.

Arch's (and Fedora's) NSS packages are integrated with p11-kit, so they should automatically pick up any certificates used system-wide. But if you prefer (or if your distro uses "pure" NSS), you can install certificates into your own browser profile as well – use certutil for this:

```
certutil -d __database__ -A -i oxo-ca.crt -n "Oxodao" -t C,,
```

Chromium and Evolution use the "shared" database at -d "sql:$HOME/.pki/nssdb".

For Firefox, Thunderbird, and SeaMonkey, specify the browser's own profile directory (e.g. -d ~/.mozilla/firefox/ov6jazas.default).

### System-wide

If it works:
```
$ sudo trust anchor --store oxo-ca.crt
```

If it doesn't (no configured writable location):
```
$ sudo cp oxo-ca.crt /etc/ca-certificates/trust-source/anchors/
$ [sudo] update-ca-trust # Not sure it requires sudo, probably
```

## Generating normal certs

### Private key
```
$ openssl genrsa -out router.lan.key 2048
```

### CSR
```
$ openssl req -new -key router.lan.key -out router.lan.csr
```

### Creating the X509 V3 certificate extension config

`router.lan.ext`
```
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = router.lan
DNS.2 = *.router.lan
```

### Signing the certificate with the Root CA certificate

```
openssl x509 -req -in router.lan.csr -CA oxo-ca.pem -CAkey oxo-ca.key -CAcreateserial -out router.lan.crt -days 825 -sha256 -extfile router.lan.ext
```

## Using the certificate

nginx

```
include snippets/ssl.conf;
ssl_certificate /path/to/certs/router.lan.crt;
ssl_certificate_key /path/to/certs/router.lan.key;
```
