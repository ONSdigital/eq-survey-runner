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
  over5: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -5,
      },
    },
  },
  under4: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -4,
      },
    },
  },
  under3: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -3,
      },
    },
  },
  under1: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -1,
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
  hasWorked: {
    id: 'ever-worked-answer',
    condition: 'not equals any',
    values: ['No, has never worked', 'No, have never worked'],
  },
    hasNotWorked: {
    id: 'ever-worked-answer',
    condition: 'equals any',
    values: ['No, has never worked', 'No, have never worked'],
  },
    working: {
    id: 'employment-status-answer',
    condition: 'not equals any',
    values: ['None of these apply'],
  },
}
