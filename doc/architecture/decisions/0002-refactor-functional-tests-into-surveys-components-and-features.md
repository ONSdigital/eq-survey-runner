# 2. Refactor functional tests into surveys, components and features

Date: 27/06/2017

## Status

Proposed

## Context

The functional tests should be organised in such a way that encourages consistent testing of components and coverage of all features of survey runner.

## Decision

- Organise test specifications (.spec.js files) under a surveys, components or features folder:
```
tests/
  functional/
    spec/
        surveys/
            census-household.spec.js
            mci.spec.js
            ...
        components/
            radio.spec.js
            checkbox.spec.js
            ...
        features/
            navigation.spec.js
            save-and-resume.spec.js
            ...
```
- Create a consistent set of tests for each component e.g. TextField, Currency, Dates etc. Each component should test:
    - Optional/mandatory
    - Saved data is persisted
    - Summary screen content
    - Summary screen updates after answer changes
    - Component specific tests e.g. other field on radio/checkbox answers
- Create a set of tests for each feature
    - Final confirmation/Summary
    - Navigation
    - Save and Resume
    - Timeout
    - Routing
    - Language
- One spec file for each survey, component or feature

- The JSON schemas will remain in the data directory so they are accessible by both users of the service and the functional tests.
- The component level schemas will be named `component_<component_name>.json` and feature schemas will be named `feature_<feature_name>.json`. This will help group related schemas together.

## Consequences

Tests are easily understood.

It is easy to identify tests that are common among components.

Survey runner features are more clearly understood.

Longer term when we have confidence in the coverage of the component and feature level tests, we can consider dropping the survey specific functional tests.
