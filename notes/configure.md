# Configuration

https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py

## Custom Fields

Simplest: https://inveniordm.docs.cern.ch/customize/custom_fields/records/
Reference: https://inveniordm.docs.cern.ch/reference/widgets/#autocompletedropdown
Build your own: https://inveniordm.docs.cern.ch/develop/howtos/custom_fields/

Managed to build a custom "Academic Programs" field in around an hour that uses a vocabulary, autocompletes on the form, and has a custom display template linking to search results sharing the same value (similar to how we do it in VAULT). The only thing that did not work is that the search facet does not appear, but the indexing clearly works because the hyperlinked search returns results.

One other disappointment is that, though I defined a bunch of properties in for each term in the related programs vocab, it only records the `id` and `title` in the record.
