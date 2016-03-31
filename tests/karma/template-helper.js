import fetch from 'node-fetch'
import bluebird from 'bluebird'

fetch.Promise = bluebird

export default function(template, data) {
  return fetch('http://localhost:5000/dev/render-template', {
    method: 'POST',
    mode: 'no-cors',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      template: template,
      data: data
    })
  })
  .then(data => data.text())
  .then(text => {
    let wrapper = document.createElement('div')
    wrapper.innerHTML = text
    return wrapper.firstChild
  })
  .catch(err => {
    console.log(err)
  })
}
