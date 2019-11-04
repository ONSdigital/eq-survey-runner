local placeholders = import '../../../lib/placeholders.libsonnet';
local rules = import 'rules.libsonnet';


{
  type: 'Question',
  id: 'visitor-sex',
  question: {
    id: 'visitor-sex-question',
    title: {
      text: 'What is {person_name_possessive} sex?',
      placeholders: [
        placeholders.personNamePossessive,
      ],
    },
    type: 'General',
    answers: [
      {
        id: 'visitor-sex-answer',
        mandatory: false,
        options: [
          {
            label: 'Female',
            value: 'Female',
          },
          {
            label: 'Male',
            value: 'Male',
          },
        ],
        type: 'Radio',
      },
    ],
  },
}
