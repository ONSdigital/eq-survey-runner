local placeholders = import '../../../lib/placeholders.libsonnet';

local questionTitle = {
  text: 'Was anyone in your current household usually living at {address} on Sunday 13 October 2019?',
  placeholders: [
    placeholders.address,
  ],
};

{
  type: 'Question',
  id: 'anyone-else-usually-living',
  show_on_section_summary: false,
  question: {
    id: 'anyone-else-usually-living-question',
    title: questionTitle,
    type: 'General',
    answers: [{
      id: 'anyone-else-usually-living-answer',
      mandatory: false,
      options: [
        {
          label: 'Yes',
          value: 'Yes',
        },
        {
          label: 'No',
          value: 'No',
        },
      ],
      type: 'Radio',
    }],
  },
  routing_rules: [
    {
      goto: {
        block: 'another-address-interviewer-note-interstitial',
        when: [
          {
            id: 'anyone-else-usually-living-answer',
            condition: 'equals',
            value: 'No',
          },
        ],
      },
    },
    {
      goto: {
        block: 'interviewer-note-interstitial',
      },
    },
  ],
}
