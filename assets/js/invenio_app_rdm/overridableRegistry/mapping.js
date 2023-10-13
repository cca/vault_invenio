/**
 * Add here all the overridden components of your app.
 * Example from Zenodo:
 * https://github.com/zenodo/zenodo-rdm/blob/master/assets/js/invenio_app_rdm/overridableRegistry/mapping.js#L3
 */

export const overriddenComponents = {
    "InvenioAppRdm.Deposit.FundingField.layout": () => null,
    "InvenioAppRdm.Deposit.LanguagesField.layout": () => null,
    "InvenioAppRdm.Deposit.VersionField.layout": () => null,
    "InvenioAppRdm.Deposit.PublisherField.layout": () => null,
    "InvenioAppRdm.Deposit.IdentifiersField.layout": () => null,
    // ? do we want to retain this actually? Might be useful for Libraries records.
    "InvenioAppRdm.Deposit.RelatedWorksField.layout": () => null,
}

// @TODO Funders, Alternate Identifiers, and Related Works all have empty
// AccordionField headers after we have removed the child overridable components
// This PR fixes: https://github.com/inveniosoftware/invenio-app-rdm/pull/2087
