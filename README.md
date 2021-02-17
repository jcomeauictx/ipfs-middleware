# ipfs-middleware: simple proxy to bypass DNS blocking of ipfs.io

 1. Add `127.227.227.227 ipfs.io` to  /etc/hosts.
 2. Use [these instructions](https://medium.com/@jedri/how-to-trust-a-ca-only-for-a-specific-domain-567ab9333c9d) to cross-sign the certificate for ipfs.io
 3. Configure nginx for ipfs.io
