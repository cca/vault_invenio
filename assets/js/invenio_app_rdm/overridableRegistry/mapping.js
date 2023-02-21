// This file is part of InvenioRDM
// Copyright (C) 2023 CERN.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

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
    "InvenioAppRdm.Deposit.RelatedWorksField.layout": () => null,
}

// @TODO Funders, Alternate Identifiers, and Related Works all have empty
// AccordionField headers after we have removed the child overridable components
// It would also be nice to override some of these fields for certain record types
// or within certain communities (e.g. Libraries could show all of them)
