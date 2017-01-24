export const getNextSiblings = function(e, filter) {
  let siblings = []
  while ((e = e.nextSibling)) { if (!filter || filter(e)) siblings.push(e) }
  return siblings
}
export const getPreviousSiblings = function(e, filter) {
  let siblings = []
  while ((e = e.previousSibling)) { if (!filter || filter(e)) siblings.push(e) }
  return siblings
}
