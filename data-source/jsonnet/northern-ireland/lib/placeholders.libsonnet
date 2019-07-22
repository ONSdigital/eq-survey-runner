{
  personName: {
    placeholder: 'person_name',
    transforms: [{
      transform: 'concatenate_list',
      arguments: {
        list_to_concatenate: {
          source: 'answers',
          identifier: ['first-name', 'last-name'],
        },
        delimiter: ' ',
      },
    }],
  },
  personNamePossessive: {
    placeholder: 'person_name_possessive',
    transforms: [
      {
        transform: 'concatenate_list',
        arguments: {
          list_to_concatenate: {
            source: 'answers',
            identifier: ['first-name', 'last-name'],
          },
          delimiter: ' ',
        },
      },
      {
        transform: 'format_possessive',
        arguments: {
          string_to_format: {
            source: 'previous_transform',
          },
        },
      },
    ],
  },
  address: {
    placeholder: 'address',
    value: {
      identifier: 'display_address',
      source: 'metadata',
    },
  },
}
