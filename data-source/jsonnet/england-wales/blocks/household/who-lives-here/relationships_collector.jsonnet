local rules = import '../../../lib/rules.libsonnet';

local first_person_placeholder = {
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
};

local second_person_placeholder = {
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
};

local first_person_name_possessive_placeholder = {
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
};

{
  type: 'RelationshipCollector',
  id: 'relationships',
  title: 'Household relationships',
  for_list: 'household',
  skip_conditions: [
    {
      when: [
        {
          list: 'household',
          condition: 'less than',
          value: 2,
        },
      ],
    },
  ],
  question_variants: [
    {
      question: {
        id: 'relationship-question',
        type: 'General',
        title: {
          text: '{second_person_name} is your <em>...</em>',
          placeholders: [second_person_placeholder]
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [{
          id: 'relationship-answer',
          mandatory: false,
          type: 'Relationship',
          playback: {
            text: '{second_person_name} is your <em>...</em>',
            placeholders: [second_person_placeholder]
          },
          options: [{
              label: 'Husband or wife',
              playback: {
                text: '{second_person_name} is your <em>husband or wife</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>husband or wife</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Husband or wife',
            },
            {
              label: 'Legally registered civil partner',
              playback: {
                text: '{second_person_name} is your <em>legally registered civil partner</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>legally registered civil partner</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Legally registered civil partner',
            },
            {
              label: 'Partner',
              playback: {
                text: '{second_person_name} is your <em>partner</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>partner</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Partner',
            },
            {
              label: 'Son or daughter',
              playback: {
                text: '{second_person_name} is your <em>son or daughter</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>son or daughter</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Son or daughter',
            },
            {
              label: 'Stepchild',
              playback: {
                text: '{second_person_name} is your <em>stepchild</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>stepchild</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Stepchild',
            },
            {
              label: 'Brother or sister',
              playback: {
                text: '{second_person_name} is your <em>brother or sister</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>brother or sister</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Brother or sister',
            },
            {
              label: 'Mother or father',
              playback: {
                text: '{second_person_name} is your <em>mother or father</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>mother or father</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Mother or father',
            },
            {
              label: 'Stepmother or stepfather',
              playback: {
                text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Stepmother or stepfather',
            },
            {
              label: 'Grandchild',
              playback: {
                text: '{second_person_name} is your <em>grandchild</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>grandchild</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Grandchild',
            },
            {
              label: 'Grandparent',
              playback: {
                text: '{second_person_name} is your <em>grandparent</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>grandparent</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Grandparent',
            },
            {
              label: 'Other relation',
              playback: {
                text: '{second_person_name} is your <em>other relation</em>',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is your <em>other relation</em>',
                placeholders: [second_person_placeholder]
              },
              value: 'Other relation',
            },
            {
              label: 'Unrelated',
              playback: {
                text: '{second_person_name} is <em>unrelated</em> to you',
                placeholders: [second_person_placeholder]
              },
              title: {
                text: '{second_person_name} is <em>unrelated</em> to you',
                placeholders: [second_person_placeholder]
              },
              value: 'Unrelated',
            },
          ],
        }, ],
      },
      when: [rules.isPrimary],
    },
    {
      question: {
        id: 'relationship-question',
        type: 'General',
        title: {
          text: 'Thinking of {first_person_name}, {second_person_name} is their <em>...</em>',
          placeholders: [first_person_placeholder, second_person_placeholder]
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [{
          id: 'relationship-answer',
          mandatory: false,
          type: 'Relationship',
          playback: {
            text: '{second_person_name} is your <em>...</em>',
            placeholders: [second_person_placeholder]
          },
          options: [{
              label: 'Husband or wife',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Husband or wife',
            },
            {
              label: 'Legally registered civil partner',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Legally registered civil partner',
            },
            {
              label: 'Partner',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>partner</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>partner</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Partner',
            },
            {
              label: 'Son or daughter',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Son or daughter',
            },
            {
              label: 'Stepchild',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>stepchild</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepchild</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Stepchild',
            },
            {
              label: 'Brother or sister',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>brother or sister</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>brother or sister</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Brother or sister',
            },
            {
              label: 'Mother or father',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>mother or father</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>mother or father</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Mother or father',
            },
            {
              label: 'Stepmother or stepfather',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>stepmother or stepfather</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepmother or stepfather</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Stepmother or stepfather',
            },
            {
              label: 'Grandchild',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>grandchild</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandchild</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Grandchild',
            },
            {
              label: 'Grandparent',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>grandparent</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandparent</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Grandparent',
            },
            {
              label: 'Other relation',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>other relation</em>',
                placeholders: [second_person_placeholder, first_person_name_possessive_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>other relation</em>',
                placeholders: [first_person_placeholder, second_person_placeholder]
            },
              value: 'Other relation',
            },
            {
              label: 'Unrelated',
              playback: {
                text: '{second_person_name} is <em>unrelated</em> to {first_person_name}',
                placeholders: [second_person_placeholder, first_person_placeholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is <em>unrelated</em> to {first_person_name}',
                placeholders: [first_person_placeholder, second_person_placeholder, first_person_placeholder]
            },
              value: 'Unrelated',
            },
          ],
        },
        ],
      },
      when: [rules.isNotPrimary],
    },
  ],
}
