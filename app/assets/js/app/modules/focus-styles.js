import domready from './domready'

const focusableClass = 'js-focusable'
const focusableBoxClass = 'js-focusable-box'
const focusClass = 'has-focus'
const checkedClass = 'is-checked'

domready(() => {
  // apply classes to existing elements on page load
  $(`.${focusableClass}:checked`).closest(`.${focusableBoxClass}`).addClass(checkedClass)

  $(`.${focusableClass}`).on({
    'focus': function() {
      $(this).parents(`.${focusableBoxClass}`).addClass(focusClass)
    },
    'blur': function() {
      $(this).parents(`.${focusableBoxClass}`).removeClass(focusClass)
    },
    'change': function() {
      const $this = $(this)
      const $closestFocusableBox = $this.closest(`.${focusableBoxClass}`)
      $closestFocusableBox.toggleClass(checkedClass, $this.is(':checked'))
      if ($this.attr('type') === 'radio') {
        // uncheck siblings
        $closestFocusableBox.siblings(`.${focusableBoxClass}`).removeClass(checkedClass)
      }
    }
  })
})
