import 'babel-polyfill'
import './parsley-config'
import Parsley from 'parsleyjs'

$('[data-guidance]').each((index, el) => {
  const $el = $(el)
  $el.find('[data-guidance-trigger]').on('click', (e) => {
    e.preventDefault()
    $el.find('[data-guidance-main]').addClass('is-visible')
    return false
  })
})
