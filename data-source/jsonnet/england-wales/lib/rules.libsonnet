{
  proxyNo: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No',
  },
  proxyYes: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes',
  },
  over19: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -19,
      },
    },
  },
  over16: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -16,
      },
    },
  },
  over15: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -15,
      },
    },
  },
  under5: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -5,
      },
    },
  },
  under4: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -4,
      },
    },
  },
  under3: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -3,
      },
    },
  },
  under1: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -1,
      },
    },
  },
  mainJob: {
    id: 'employment-status-answer-exclusive',
    condition: 'not set',
  },
  lastMainJob: {
    id: 'employment-status-answer-exclusive',
    condition: 'contains',
    value: 'None of these apply',
  },
  accommodationIsHouse: {
    id: 'accommodation-type-answer',
    condition: 'equals',
    value: 'Whole house or bungalow',
  },
  accommodationIsFlat: {
    id: 'accommodation-type-answer',
    condition: 'equals',
    value: 'Flat, maisonette or apartment',
  },
  accomodationNotAnswered: {
    id: 'accomodation-type-answer',
    condition: 'not set',
  },
  isPrimary: {
    list: 'household',
    id_selector: 'primary_person',
    condition: 'equals',
    comparison: {
      source: 'location',
      id: 'list_item_id',
    },
  },
  isNotPrimary: {
    list: 'household',
    id_selector: 'primary_person',
    condition: 'not equals',
    comparison: {
      source: 'location',
      id: 'list_item_id',
    },
  },
  hasPrimary: {
    id: 'you-live-here-answer',
    condition: 'equals',
    value: 'Yes, I usually live here',
  },
  firstPersonPlaceholder: {
    placeholder: 'first_person_name',
    'transforms': [{
      'transform': 'concatenate_list',
      'arguments': {
        'list_to_concatenate': {
          'source': 'answers',
          'identifier': ['first-name', 'last-name'],
          'list_item_selector': {
            'source': 'location',
            'id': 'list_item_id'
          }
        },
        'delimiter': ' '
      }
    }]
  },
  secondPersonPlaceholder: {
    placeholder: 'second_person_name',
    'transforms': [{
      'transform': 'concatenate_list',
      'arguments': {
        'list_to_concatenate': {
          'source': 'answers',
          'identifier': ['first-name', 'last-name'],
          'list_item_selector': {
            'source': 'location',
            'id': 'to_list_item_id'
          }
        },
        'delimiter': ' '
      }
    }]
  },
  firstPersonNamePossessivePlaceholder: {
    'placeholder': 'first_person_name_possessive',
    'transforms': [{
        'transform': 'concatenate_list',
        'arguments': {
          'list_to_concatenate': {
            'source': 'answers',
            'identifier': ['first-name', 'last-name'],
            'list_item_selector': {
              'source': 'location',
              'id': 'list_item_id'
            }
          },
          'delimiter': ' '
        }
      },
      {
        'transform': 'format_possessive',
        'arguments': {
          'string_to_format': {
            'source': 'previous_transform'
          }
        }
      }
    ]
  },
}


