export default function getTransitionEndEvent() {
  const el = document.createElement('fakeelement')
  const transitions = {
    'transition': 'transitionend',
    'OTransition': 'oTransitionEnd',
    'MozTransition': 'transitionend',
    'WebkitTransition': 'webkitTransitionEnd'
  }

  for (let t in transitions) {
    if (el.style[t] !== undefined) {
      return transitions[t]
    }
  }
}
