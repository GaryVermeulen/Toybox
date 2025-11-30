graph [
  directed 1
  name "Space"
  node [
    id 0
    label "space"
  ]
  node [
    id 1
    label "universe"
  ]
  node [
    id 2
    label "galaxy"
  ]
  node [
    id 3
    label "star"
  ]
  node [
    id 4
    label "planet"
  ]
  node [
    id 5
    label "earth"
  ]
  node [
    id 6
    label "park"
  ]
  edge [
    source 0
    target 1
    label "associated"
  ]
  edge [
    source 1
    target 2
    label "associated"
  ]
  edge [
    source 2
    target 3
    label "associated"
  ]
  edge [
    source 3
    target 4
    label "associated"
  ]
  edge [
    source 4
    target 5
    label "associated"
  ]
  edge [
    source 5
    target 6
    label "associated"
  ]
]
