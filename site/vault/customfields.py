from invenio_rdm_records.config import RDM_FACETS, RDM_SEARCH
from invenio_records_resources.services.records.facets import CFTermsFacet
from invenio_vocabularies.services.custom_fields import VocabularyCF

RDM_NAMESPACES = {
    "cca": "https://www.cca.edu/",
}

RDM_CUSTOM_FIELDS = [
    VocabularyCF(  # the type of custom field, VocabularyCF is a controlled vocabulary
        name="cca:program",  # name of the field, namespaced by `cern`
        vocabulary_id="programs",  # controlled vocabulary id defined in the vocabularies.yaml file
        dump_options=True,  # True when the list of all possible values will be visible in the dropdown UI component, typically for small vocabularies
        multiple=False, # if the field accepts a list of values (True) or single value (False)
    ),
]

RDM_CUSTOM_FIELDS_UI = [
    {
        "section": "CCA Custom Fields",
        "fields": [
            dict(
                field="cca:program",
                ui_widget="AutocompleteDropdown",
                template="program.html",
                props=dict(
                    label="Academic Program",
                    placeholder="Animation Program",
                    icon="building",
                    description="Select one of CCA's academic programs",
                    autocompleteFrom="/api/vocabularies/programs",
                    autocompleteFromAcceptHeader="application/vnd.inveniordm.v1+json",
                    multiple=False,   # True for selecting multiple values
                    clearable=True,
                )
            ),
        ]
    }
]

RDM_FACETS = {
    **RDM_FACETS,
    "program": {
        "facet": CFTermsFacet(  # backend facet
            field="cca:programs.id",  # id is the keyword field of a vocabulary
            label="Academic Program",
        ),
        "ui": {  # ui display
            "field": CFTermsFacet.field("cca:programs.id"),
        },
    },
}

RDM_SEARCH = {
    **RDM_SEARCH,
    "facets": RDM_SEARCH["facets"] + ["program"]
}
