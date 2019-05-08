# 8. Lookups

## Context

We need to be able to specify a lookup component within a runner schema. These are to be used to provide a dropdown list of suggestions and simple entry before a user enters the full answer text.

## Decision

We will define a new answer type 'Lookup' within the schema which identifies the answer should be rendered as a lookup component.

    {
        id: 'religion-question',
        title: 'What is your religion?',
        description: 'This question is voluntary',
        type: 'General',
        answers: [
          {
            id: 'religion-answer',
            mandatory: false,
            label: 'Religion',
            type: 'Lookup',
            lookup_type: 'Religion'
          }
        ]
    }

The answer behaves as a Textfield and specifies a `lookup_type` reference to a configuration value in runner used to determine a api url.

The api url will then be passed to the frontend component to retrieve suggestions from when JavaScript is enabled.

### REST Service

The api to query is a service that takes an input string and returns a single flat array of suggestion strings. 

Initially there will be no authentication.

One service is expected to host all single tier lookups.

The region code is supplied as a query parameter and understood by the service in order to provide language variations when available.

## Consequences

- Lookups are able to be represented within a schema.
- Lookup urls are not hardcoded and able to be specified per environment
