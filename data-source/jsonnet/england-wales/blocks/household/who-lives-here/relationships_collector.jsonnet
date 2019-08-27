local rules = import '../../../lib/rules.libsonnet';

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
          placeholders: [rules.secondPersonPlaceholder]
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [{
          id: 'relationship-answer',
          mandatory: false,
          type: 'Relationship',
          playback: {
            text: '{second_person_name} is your <em>...</em>',
            placeholders: [rules.secondPersonPlaceholder]
          },
          options: [{
              label: 'Husband or wife',
              playback: {
                text: '{second_person_name} is your <em>husband or wife</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>husband or wife</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Husband or wife',
            },
            {
              label: 'Legally registered civil partner',
              playback: {
                text: '{second_person_name} is your <em>legally registered civil partner</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>legally registered civil partner</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Legally registered civil partner',
            },
            {
              label: 'Partner',
              playback: {
                text: '{second_person_name} is your <em>partner</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>partner</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Partner',
            },
            {
              label: 'Son or daughter',
              playback: {
                text: '{second_person_name} is your <em>son or daughter</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>son or daughter</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Son or daughter',
            },
            {
              label: 'Stepchild',
              playback: {
                text: '{second_person_name} is your <em>stepchild</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>stepchild</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Stepchild',
            },
            {
              label: 'Brother or sister',
              playback: {
                text: '{second_person_name} is your <em>brother or sister</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>brother or sister</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Brother or sister',
            },
            {
              label: 'Mother or father',
              playback: {
                text: '{second_person_name} is your <em>mother or father</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>mother or father</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Mother or father',
            },
            {
              label: 'Stepmother or stepfather',
              playback: {
                text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>stepmother or stepfather</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Stepmother or stepfather',
            },
            {
              label: 'Grandchild',
              playback: {
                text: '{second_person_name} is your <em>grandchild</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>grandchild</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Grandchild',
            },
            {
              label: 'Grandparent',
              playback: {
                text: '{second_person_name} is your <em>grandparent</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>grandparent</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Grandparent',
            },
            {
              label: 'Other relation',
              playback: {
                text: '{second_person_name} is your <em>other relation</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is your <em>other relation</em>',
                placeholders: [rules.secondPersonPlaceholder]
              },
              value: 'Other relation',
            },
            {
              label: 'Unrelated',
              playback: {
                text: '{second_person_name} is <em>unrelated</em> to you',
                placeholders: [rules.secondPersonPlaceholder]
              },
              title: {
                text: '{second_person_name} is <em>unrelated</em> to you',
                placeholders: [rules.secondPersonPlaceholder]
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
          placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
        },
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [{
          id: 'relationship-answer',
          mandatory: false,
          type: 'Relationship',
          playback: {
            text: '{second_person_name} is your <em>...</em>',
            placeholders: [rules.secondPersonPlaceholder]
          },
          options: [{
              label: 'Husband or wife',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Husband or wife',
            },
            {
              label: 'Legally registered civil partner',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Legally registered civil partner',
            },
            {
              label: 'Partner',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>partner</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>partner</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Partner',
            },
            {
              label: 'Son or daughter',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Son or daughter',
            },
            {
              label: 'Stepchild',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>stepchild</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepchild</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Stepchild',
            },
            {
              label: 'Brother or sister',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>brother or sister</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>brother or sister</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Brother or sister',
            },
            {
              label: 'Mother or father',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>mother or father</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>mother or father</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Mother or father',
            },
            {
              label: 'Stepmother or stepfather',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>stepmother or stepfather</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepmother or stepfather</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Stepmother or stepfather',
            },
            {
              label: 'Grandchild',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>grandchild</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandchild</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Grandchild',
            },
            {
              label: 'Grandparent',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>grandparent</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandparent</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Grandparent',
            },
            {
              label: 'Other relation',
              playback: {
                text: '{second_person_name} is {first_person_name_possessive} <em>other relation</em>',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonNamePossessivePlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is their <em>other relation</em>',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder]
            },
              value: 'Other relation',
            },
            {
              label: 'Unrelated',
              playback: {
                text: '{second_person_name} is <em>unrelated</em> to {first_person_name}',
                placeholders: [rules.secondPersonPlaceholder, rules.firstPersonPlaceholder]
              },
              title: {
                text: 'Thinking of {first_person_name}, {second_person_name} is <em>unrelated</em> to {first_person_name}',
                placeholders: [rules.firstPersonPlaceholder, rules.secondPersonPlaceholder, rules.firstPersonPlaceholder]
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
