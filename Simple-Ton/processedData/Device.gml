graph [
  directed 1
  name "Device"
  node [
    id 0
    label "device"
  ]
  node [
    id 1
    label "instrument"
  ]
  node [
    id 2
    label "computer"
  ]
  node [
    id 3
    label "machine"
  ]
  node [
    id 4
    label "vechile"
  ]
  node [
    id 5
    label "SimpleTon"
  ]
  node [
    id 6
    label "telescope"
  ]
  edge [
    source 0
    target 1
    label "associated"
  ]
  edge [
    source 0
    target 2
    label "associated"
  ]
  edge [
    source 0
    target 3
    label "associated"
  ]
  edge [
    source 1
    target 6
    label "associated"
  ]
  edge [
    source 2
    target 5
    label "associated"
  ]
  edge [
    source 3
    target 4
    label "associated"
  ]
]
