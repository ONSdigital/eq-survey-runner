import sampleSize from 'lodash/sampleSize'

export const getUri = uri => browser.options.baseUrl + uri

export const getRandomString = length => sampleSize('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', length).join('')
