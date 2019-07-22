{
  proxyNo: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'For myself',
  },
  proxyYes: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'For someone else',
  },
  over16: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -16,
      },
    },
  },
  mainJob: {
    id: 'employment-status-answer-exclusive',
    condition: 'not set',
  },
  lastMainJob: {
    id: 'employment-status-answer-exclusive',
    condition: 'contains',
    value: 'None of these apply',
  },
}
