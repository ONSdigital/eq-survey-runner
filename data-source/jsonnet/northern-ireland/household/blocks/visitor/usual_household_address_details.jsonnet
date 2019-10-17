local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';


{
  type: 'Question',
  id: 'usual-address-details',
  question: {
    id: 'usual-address-details-question',
    title: {
      text: 'Enter details of <em>{person_name_possessive}</em> usual UK address',
      placeholders: [
        placeholders.personNamePossessive,
      ],
    },
    type: 'General',
    answers: [
      {
        id: 'usual-address-details-answer-building',
        label: 'Address line 1',
        mandatory: false,
        autocomplete: 'address-line1',
        type: 'TextField',
      },
      {
        id: 'usual-address-details-answer-street',
        label: 'Address line 2',
        mandatory: false,
        autocomplete: 'address-line2',
        type: 'TextField',
      },
      {
        id: 'usual-address-details-answer-city',
        label: 'Town or city',
        mandatory: false,
        autocomplete: 'address-line3',
        type: 'TextField',
      },
      {
        id: 'usual-address-details-answer-county',
        label: 'County (optional)',
        mandatory: false,
        type: 'TextField',
      },
      {
        id: 'usual-address-details-answer-postcode',
        label: 'Postcode',
        mandatory: false,
        autocomplete: 'postal-code',
        type: 'TextField',
      },
    ],
  },
}
