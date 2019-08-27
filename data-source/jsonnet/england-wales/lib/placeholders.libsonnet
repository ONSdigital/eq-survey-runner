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
  censusDate(census_date): {
    placeholder: 'census_date',
    transforms: [{
      transform: 'format_date',
      arguments: {
        date_to_format: {
          value: census_date,
        },
        date_format: 'd MMMM yyyy',
      },
    }],
  },
  firstPersonPlaceholder: {
    placeholder: 'first_person_name',
    transforms: [{
      transform: 'concatenate_list',
      arguments: {
        list_to_concatenate: {
          source: 'answers',
          identifier: ['first-name', 'last-name'],
          list_item_selector: {
            source: 'location',
            id: 'list_item_id'
          }
        },
        delimiter: ' '
      }
    }]
  },
  secondPersonPlaceholder: {
    placeholder: 'second_person_name',
    transforms: [{
      transform: 'concatenate_list',
      arguments: {
        list_to_concatenate: {
          source: 'answers',
          identifier: ['first-name', 'last-name'],
          list_item_selector: {
            source: 'location',
            id: 'to_list_item_id'
          }
        },
        delimiter: ' '
      }
    }]
  },
  firstPersonNamePossessivePlaceholder: {
    placeholder: 'first_person_name_possessive',
    transforms: [{
        transform: 'concatenate_list',
        arguments: {
          list_to_concatenate: {
            source: 'answers',
            identifier: ['first-name', 'last-name'],
            list_item_selector: {
              source: 'location',
              id: 'list_item_id'
            }
          },
          delimiter: ' '
        }
      },
      {
        transform: 'format_possessive',
        arguments: {
          string_to_format: {
            source: 'previous_transform'
          }
        }
      }
    ]
  },
}
