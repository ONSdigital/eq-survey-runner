local placeholders = import '../../../lib/placeholders.libsonnet';

local questionTitle = {
  text: 'Is there any other living accommodation at {address}?',
  placeholders: [
    placeholders.address,
  ],
};

{
  type: 'Question',
  id: 'other-living-accommodation',
  question: {
    id: 'other-living-accommodation-question',
    title: questionTitle,
    type: 'General',
    guidance: {
      contents: [
        {
          description: 'For example, separate bedsits, annexes, sheds etc.',
        },
      ],
    },
    instruction: 'If “Yes” ensure this accommodation is recorded on the Fieldwork Management Tool and interview household separately',
    answers: [{
      id: 'other-living-accommodation-answer',
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
}
