local placeholders = import '../../../lib/placeholders.libsonnet';


{
  type: 'Interstitial',
  id: 'individual-interstitial',
  content: {
    title: {
      text: '{person_name}',
      placeholders: [
        placeholders.personName,
      ],
    },
    contents: [
      {
        description: {
          text: 'In this section, we’re going to ask you questions about <strong>{person_name}</strong>.',
          placeholders: [
            placeholders.personName,
          ],
        },
      },
      {
        title: 'You will need to know',
        list: [
          'Personal details such as date of birth, country of birth, religion etc.',
          'Education and qualifications',
          'Employment and travel to work',
          'Second or holiday homes',
          'Unpaid care and health',
          'Languages',
        ],
      },
    ],
  },
}
