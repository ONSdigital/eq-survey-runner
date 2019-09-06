local rules = import 'rules.libsonnet';

local firstPersonPlaceholder = {
  placeholder: 'first_person_name',
  transforms: [{
    transform: 'concatenate_list',
    arguments: {
      list_to_concatenate: {
        source: 'answers',
        identifier: ['first-name', 'last-name'],
        list_item_selector: {
          source: 'location',
          id: 'list_item_id',
        },
      },
      delimiter: ' ',
    },
  }],
};

local secondPersonPlaceholder = {
  placeholder: 'second_person_name',
  transforms: [{
    transform: 'concatenate_list',
    arguments: {
      list_to_concatenate: {
        source: 'answers',
        identifier: ['first-name', 'last-name'],
        list_item_selector: {
          source: 'location',
          id: 'to_list_item_id',
        },
      },
      delimiter: ' ',
    },
  }],
};

local firstPersonNamePossessivePlaceholder = {
  placeholder: 'first_person_name_possessive',
  transforms: [
    {
      transform: 'concatenate_list',
      arguments: {
        list_to_concatenate: {
          source: 'answers',
          identifier: ['first-name', 'last-name'],
          list_item_selector: {
            source: 'location',
            id: 'list_item_id',
          },
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
          text: '{second_person_name} is your <em>…</em>',
          placeholders: [secondPersonPlaceholder],
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [
          {
            id: 'relationship-answer',
            mandatory: false,
            type: 'Relationship',
            playback: {
              text: '{second_person_name} is your <em>…</em>',
              placeholders: [secondPersonPlaceholder],
            },
            options: [
              {
                label: 'Husband or wife',
                playback: {
                  text: '{second_person_name} is your <em>husband or wife</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>husband or wife</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Husband or wife',
              },
              {
                label: 'Same-sex civil partner',
                playback: {
                  text: '{second_person_name} is your <em>Same-sex civil partner</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>Same-sex civil partner</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Same-sex civil partner',
              },
              {
                label: 'Partner',
                playback: {
                  text: '{second_person_name} is your <em>partner</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>partner</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Partner',
              },
              {
                label: 'Son or daughter',
                playback: {
                  text: '{second_person_name} is your <em>son or daughter</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>son or daughter</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Son or daughter',
              },
              {
                label: 'Stepchild',
                playback: {
                  text: '{second_person_name} is your <em>stepchild</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>stepchild</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Stepchild',
              },
              {
                description: 'Including half brother or half sister',
                label: 'Brother or sister',
                playback: {
                  text: '{second_person_name} is your <em>brother or sister</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>brother or sister</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Brother or sister',
              },
              {
                label: 'Stepbrother or stepsister',
                playback: {
                  text: '{second_person_name} is your <em>stepbrother or stepsister</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>stepbrother or stepsister</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Stepbrother or stepsister',
              },
              {
                label: 'Mother or father',
                playback: {
                  text: '{second_person_name} is your <em>mother or father</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>mother or father</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Mother or father',
              },
              {
                label: 'Stepmother or stepfather',
                playback: {
                  text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Stepmother or stepfather',
              },
              {
                label: 'Grandchild',
                playback: {
                  text: '{second_person_name} is your <em>grandchild</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>grandchild</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Grandchild',
              },
              {
                label: 'Grandparent',
                playback: {
                  text: '{second_person_name} is your <em>grandparent</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>grandparent</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Grandparent',
              },
              {
                label: 'Other relation',
                playback: {
                  text: '{second_person_name} is your <em>other relation</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is your <em>other relation</em>',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Other relation',
              },
              {
                description: 'Including foster child',
                label: 'Unrelated',
                playback: {
                  text: '{second_person_name} is <em>unrelated</em> to you',
                  placeholders: [secondPersonPlaceholder],
                },
                title: {
                  text: '{second_person_name} is <em>unrelated</em> to you',
                  placeholders: [secondPersonPlaceholder],
                },
                value: 'Unrelated',
              },
            ],
          },
        ],
      },
      when: [rules.isPrimary],
    },
    {
      question: {
        id: 'relationship-question',
        type: 'General',
        title: {
          text: 'Thinking of {first_person_name}, {second_person_name} is their <em>…</em>',
          placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [
          {
            id: 'relationship-answer',
            mandatory: false,
            type: 'Relationship',
            playback: {
              text: '{second_person_name} is {first_person_name_possessive} <em>…</em>',
              placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
            },
            options: [
              {
                label: 'Husband or wife',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Husband or wife',
              },
              {
                label: 'Same-sex civil partner',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>Same-sex civil partner</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>Same-sex civil partner</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Same-sex civil partner',
              },
              {
                label: 'Partner',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>partner</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>partner</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Partner',
              },
              {
                label: 'Son or daughter',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Son or daughter',
              },
              {
                label: 'Stepchild',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>stepchild</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepchild</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Stepchild',
              },
              {
                description: 'Including half brother or half sister',
                label: 'Brother or sister',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>brother or sister</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>brother or sister</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Brother or sister',
              },
              {
                label: 'Stepbrother or stepsister',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>stepbrother or stepsister</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepbrother or stepsister</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Stepbrother or stepsister',
              },
              {
                label: 'Mother or father',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>mother or father</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>mother or father</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Mother or father',
              },
              {
                label: 'Stepmother or stepfather',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>stepmother or stepfather</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepmother or stepfather</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Stepmother or stepfather',
              },
              {
                label: 'Grandchild',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>grandchild</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandchild</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Grandchild',
              },
              {
                label: 'Grandparent',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>grandparent</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandparent</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Grandparent',
              },
              {
                label: 'Other relation',
                playback: {
                  text: '{second_person_name} is {first_person_name_possessive} <em>other relation</em>',
                  placeholders: [secondPersonPlaceholder, firstPersonNamePossessivePlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is their <em>other relation</em>',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder],
                },
                value: 'Other relation',
              },
              {
                description: 'Including foster child',
                label: 'Unrelated',
                playback: {
                  text: '{second_person_name} is <em>unrelated</em> to {first_person_name}',
                  placeholders: [secondPersonPlaceholder, firstPersonPlaceholder],
                },
                title: {
                  text: 'Thinking of {first_person_name}, {second_person_name} is <em>unrelated</em> to {first_person_name}',
                  placeholders: [firstPersonPlaceholder, secondPersonPlaceholder, firstPersonPlaceholder],
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
