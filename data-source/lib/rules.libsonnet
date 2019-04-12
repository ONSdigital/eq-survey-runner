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
    condition: 'less than',
    date_comparison: {
      value: 'now',
      offset_by: {
        years: -16,
      },
    },
  },
  regionNotWales: {
    meta: 'region_code',
    condition: 'not equals',
    value: 'GB-WLS',
  },
  regionWales: {
    meta: 'region_code',
    condition: 'equals',
    value: 'GB-WLS',
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
