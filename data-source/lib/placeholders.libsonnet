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
    transforms: [{
      transform: 'concatenate_list',
      arguments: {
        list_to_concatenate: {
          source: 'metadata',
          identifier: ['address-line-1', 'address-line-2'],
        },
        delimiter: ', ',
      },
    }],
  },
  censusDate: {
    placeholder: 'census_date',
    transforms: [{
      transform: 'format_date',
      arguments: {
        date_to_format: {
          value: std.extVar('census_date'),
        },
        date_format: 'd MMMM YYYY',
      },
    }],
  },
}
