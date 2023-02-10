
# Custom fields
# https://inveniordm.docs.cern.ch/customize/custom_fields/records/
# and in even more detail (write your own CF class & UI widget)
# https://inveniordm.docs.cern.ch/develop/topics/custom_fields/
from invenio_rdm_records.config import RDM_FACETS, RDM_SEARCH
from invenio_records_resources.services.custom_fields import TextCF
from invenio_records_resources.services.records.facets import CFTermsFacet
from invenio_vocabularies.services.custom_fields import VocabularyCF
# https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html
from marshmallow_utils.fields import SanitizedHTML, SanitizedUnicode

RDM_NAMESPACES = {
    "cca_libraries": "https://libraries.cca.edu"
}

RDM_CUSTOM_FIELDS = [
    # list of field types
    # https://inveniordm.docs.cern.ch/customize/custom_fields/records/#field-types
    VocabularyCF(
        name="cca_libraries:academic_programs",
        vocabulary_id="CCAAP",
        dump_options=False,
        multiple=False,
    ),
    # TextCF(
    #     name="cca_libraries:artists_statement",
    # # validation for field, can also provide custom err messages
    # # this caused a build error until I commented it out
    # # "invenio_records_resources.services.custom_fields.base.BaseListCF.__init__() got multiple values for keyword argument 'field_cls'"
    #     field_cls=SanitizedHTML,
    # )
]

RDM_CUSTOM_FIELDS_UI = [
    {
        "section": _("CCA Details"),
        "fields": [
            dict(
                field="cca_libraries:academic_programs",
                # list of UI widgets
                # https://inveniordm.docs.cern.ch/customize/custom_fields/records/#ui-widgets
                ui_widget="AutocompleteDropdown",
                # can also provide a template="/my.html" in the /templates folder
                # for display of the value after publishing
                props=dict(
                    label="Academic Program",
                    placeholder="Animation, Ceramics, etc...",
                    icon="pencil",
                    description="CCA Academic Program",
                    search=True,
                    multiple=False,
                    clearable=False,
                    required=True,
                )
            ),
            # dict(
            #     field="cca_libraries:artists_statement",
            #     ui_widget="RichInput",
            #     props=dict(
            #         label="Artist's Statement",
            #         placeholder="Explain your artistic vision in 2-3 paragraphs.",
            #         icon="pencil",
            #     )
            # ),
        ]
    }
]

RDM_FACETS = {
    **RDM_FACETS,
    "academic_programs": {
        "facet": CFTermsFacet(
            field="cca_libraries:academic_programs.id",
            label=_("Academic Programs")
        ),
        "ui": {
            "field": CFTermsFacet.field("cca_libraries:academic_programs.id"),
        }
    }
}

RDM_SEARCH = {
    **RDM_SEARCH,
    "facets": RDM_SEARCH["facets"] + ["academic_programs"]
}
