# Configuration

https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py

See invenio.cfg which has numerous comments.

## Security, Users

Users are created by app_data/[users.yaml](https://inveniordm.docs.cern.ch/customize/vocabularies/users/). The default admin is admin@inveniosoftware.org with a password defined in invenio.cfg by `RDM_RECORDS_USER_FIXTURE_PASSWORDS`. Passwords in the setting override passwords in users.yaml.

There are many invenio.cfg boolean settings we'll need to flip when we switch to SSO.

- `USERPROFILES_READ_ONLY = False` set to `True` to prevent users from editing their emails?
- `ACCOUNTS_LOCAL_LOGIN_ENABLED = True` allow local accounts (versus OAuth or SSO accounts)
- `SECURITY_REGISTERABLE = True` allows users to register
- `SECURITY_RECOVERABLE = True`  allows users to reset the password
- `SECURITY_CHANGEABLE = True`  allows users to change their password

These two settings let users to sign up and login without confirming their email, which is useful during development.

- `SECURITY_CONFIRMABLE = False`  # local login: users can confirm e-mail address
- `SECURITY_LOGIN_WITHOUT_CONFIRMATION = True` # require users to confirm email before being able to login

As of v11, there is a `--confirm` flag so you can `invenio users create -c` to automatically confirm the created user.

To give an account admin permissions, run: `pipenv run invenio roles add <email> admin`

See the [SAML Integration](https://inveniordm.docs.cern.ch/customize/authentication/#saml-integration) documentation.

## Custom Fields

Simplest: https://inveniordm.docs.cern.ch/customize/custom_fields/records/
Reference: https://inveniordm.docs.cern.ch/reference/widgets/#autocompletedropdown
Build your own: https://inveniordm.docs.cern.ch/develop/howtos/custom_fields/

Managed to build a custom "Academic Programs" field in around an hour that uses a vocabulary, autocompletes on the form, and has a custom display template linking to search results sharing the same value (similar to how we do it in VAULT). The only thing that did not work is that the search facet does not appear, but the indexing clearly works because the hyperlinked search returns results.

One other disappointment is that, though I defined a bunch of properties in for each term in the related programs vocab, it only records the `id` and `title` in the record.
