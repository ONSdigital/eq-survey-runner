import 'babel-polyfill'

$('.js-details').each((index, el) => {
  const $el = $(el)
  const $trigger = $el.find('.js-details-trigger')
  $trigger.on('click', (e) => {
    e.preventDefault()
    $trigger.attr('aria-expanded', 'true')
    $el.addClass('is-expanded')
      .find('.js-details-main')
      .focus()
      .attr('aria-hidden', 'false')
    return false
  })
})
