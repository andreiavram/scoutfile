This folder should contain keys for JWT signing and confirmation. These keys are NOT stored in the repo for security reasons.

Details on JWT: https://github.com/namespace-ee/django-rest-framework-sso

To generate keys:

```bash
$ openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
$ openssl rsa -pubout -in private_key.pem -out public_key.pem
$ cat private_key.pem public_key.pem > PROJECT_ROOT/keys/scoutfile-2023.pem
```
