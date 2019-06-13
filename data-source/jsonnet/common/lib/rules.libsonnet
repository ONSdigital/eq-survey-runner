{
  proxyNo: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'No',
  },
  proxyYes: {
    id: 'proxy-answer',
    condition: 'equals',
    value: 'Yes',
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
  over15: {
    id: 'date-of-birth-answer',
    condition: 'less than or equal to',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -15,
      },
    },
  },
  under5: {
    id: 'date-of-birth-answer',
    condition: 'greater than',
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
}
