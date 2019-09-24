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
}
