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
        title: '{second_person_name} is your <em>...</em>',
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [
          {
            id: 'relationship-answer',
            mandatory: false,
            type: 'Relationship',
            playback: '{second_person_name} is your <em>...</em>',
            options: [
              {
                label: 'Husband or wife',
                playback: '{second_person_name} is your <em>husband or wife</em>',
                title: '{second_person_name} is your <em>husband or wife</em>',
                value: 'Husband or wife',
              },
              {
                label: 'Legally registered civil partner',
                playback: '{second_person_name} is your <em>legally registered civil partner</em>',
                title: '{second_person_name} is your <em>legally registered civil partner</em>',
                value: 'Legally registered civil partner',
              },
              {
                label: 'Partner',
                playback: '{second_person_name} is your <em>partner</em>',
                title: '{second_person_name} is your <em>partner</em>',
                value: 'Partner',
              },
              {
                label: 'Son or daughter',
                playback: '{second_person_name} is your <em>son or daughter</em>',
                title: '{second_person_name} is your <em>son or daughter</em>',
                value: 'Son or daughter',
              },
              {
                label: 'Stepchild',
                playback: '{second_person_name} is your <em>stepchild</em>',
                title: '{second_person_name} is your <em>stepchild</em>',
                value: 'Stepchild',
              },
              {
                label: 'Brother or sister',
                playback: '{second_person_name} is your <em>brother or sister</em>',
                title: '{second_person_name} is your <em>brother or sister</em>',
                description: 'Including half brother or half sister',
                value: 'Brother or sister',
              },
              {
                label: 'Mother or father',
                playback: '{second_person_name} is your <em>mother or father</em>',
                title: '{second_person_name} is your <em>mother or father</em>',
                value: 'Mother or father',
              },
              {
                label: 'Stepmother or stepfather',
                playback: '{second_person_name} is your <em>stepmother or stepfather</em>',
                title: '{second_person_name} is your <em>stepmother or stepfather</em>',
                value: 'Stepmother or stepfather',
              },
              {
                label: 'Grandchild',
                playback: '{second_person_name} is your <em>grandchild</em>',
                title: '{second_person_name} is your <em>grandchild</em>',
                value: 'Grandchild',
              },
              {
                label: 'Grandparent',
                playback: '{second_person_name} is your <em>grandparent</em>',
                title: '{second_person_name} is your <em>grandparent</em>',
                value: 'Grandparent',
              },
              {
                label: 'Other relation',
                playback: '{second_person_name} is your <em>other relation</em>',
                title: '{second_person_name} is your <em>other relation</em>',
                value: 'Other relation',
              },
              {
                label: 'Unrelated',
                playback: '{second_person_name} is <em>unrelated</em> to you',
                title: '{second_person_name} is <em>unrelated</em> to you',
                description: 'Including foster child',
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
        title: 'Thinking of {first_person_name}, {second_person_name} is their <em>...</em>',
        description: 'Complete the sentence by selecting the appropriate relationship.',
        answers: [
          {
            id: 'relationship-answer',
            mandatory: false,
            type: 'Relationship',
            playback: '{second_person_name} is your <em>...</em>',
            options: [
              {
                label: 'Husband or wife',
                playback: '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                value: 'Husband or wife',
              },
              {
                label: 'Legally registered civil partner',
                playback: '{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>',
                value: 'Legally registered civil partner',
              },
              {
                label: 'Partner',
                playback: '{second_person_name} is {first_person_name_possessive} <em>partner</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>partner</em>',
                value: 'Partner',
              },
              {
                label: 'Son or daughter',
                playback: '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                value: 'Son or daughter',
              },
              {
                label: 'Stepchild',
                playback: '{second_person_name} is {first_person_name_possessive} <em>stepchild</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepchild</em>',
                value: 'Stepchild',
              },
              {
                label: 'Brother or sister',
                playback: '{second_person_name} is {first_person_name_possessive} <em>brother or sister</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>brother or sister</em>',
                description: 'Including half brother or half sister',
                value: 'Brother or sister',
              },
              {
                label: 'Mother or father',
                playback: '{second_person_name} is {first_person_name_possessive} <em>mother or father</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>mother or father</em>',
                value: 'Mother or father',
              },
              {
                label: 'Stepmother or stepfather',
                playback: '{second_person_name} is {first_person_name_possessive} <em>stepmother or stepfather</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>stepmother or stepfather</em>',
                value: 'Stepmother or stepfather',
              },
              {
                label: 'Grandchild',
                playback: '{second_person_name} is {first_person_name_possessive} <em>grandchild</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandchild</em>',
                value: 'Grandchild',
              },
              {
                label: 'Grandparent',
                playback: '{second_person_name} is {first_person_name_possessive} <em>grandparent</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>grandparent</em>',
                value: 'Grandparent',
              },
              {
                label: 'Other relation',
                playback: '{second_person_name} is {first_person_name_possessive} <em>other relation</em>',
                title: 'Thinking of {first_person_name}, {second_person_name} is their <em>other relation</em>',
                value: 'Other relation',
              },
              {
                label: 'Unrelated',
                playback: '{second_person_name} is <em>unrelated</em> to {first_person_name}',
                title: 'Thinking of {first_person_name}, {second_person_name} is <em>unrelated</em> to {first_person_name}',
                description: 'Including foster child',
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
