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
          text: 'In this section, I’m going to ask you questions about {person_name}.',
          placeholders: [
            placeholders.personName,
          ],
        },
      },
    ],
  },
}
