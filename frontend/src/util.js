export class Tool {
  static Area = new Tool('Area')
  static RestrictedArea = new Tool('R_Area')
  static Move = new Tool('Move')
  static Delete = new Tool('Delete')

  constructor(name) {
    this.name = name
  }

  toString() {
    return `Tool.${this.name}`
  }
}

export class AreaCorner {
  static TopLeft = new AreaCorner('TopLeft')
  static TopRight = new AreaCorner('TopRight')
  static BottomLeft = new AreaCorner('BottomLeft')
  static BottomRight = new AreaCorner('BottomRight')

  constructor(name) {
    this.name = name
  }

  isDiagnonalTLtoBR() {
    return this.name == 'TopLeft' || this.name == 'BottomRight'
  }

  toString() {
    return `AreaCorner.${this.name}`
  }
}

export class AreaBorder {
  static Top = new AreaBorder('Top')
  static Left = new AreaBorder('Left')
  static Right = new AreaBorder('Right')
  static Bottom = new AreaBorder('Bottom')

  constructor(name) {
    this.name = name
  }

  isX() {
    return this.name == 'Left' || this.name == 'Right'
  }

  toString() {
    return `AreaBorder.${this.name}`
  }
}

export class DrawingState {
  static Waiting = new DrawingState('waiting')
  static Drawing = new DrawingState('drawing')
  static Selected = new DrawingState('selected')
  static Resize = new DrawingState('resize')
  static Strech = new DrawingState('strech')
  static Move = new DrawingState('move')

  constructor(name) {
    this.name = name
  }

  toString() {
    return `DrawingState.${this.name}`
  }
}

export class DrawingShape {
  static Area = new DrawingShape('area')
  static RestrictedArea = new DrawingShape('restricted-area')
  static Machine = new DrawingShape('machine')

  constructor(name) {
    this.name = name
  }

  toString() {
    return `DrawingShape.${this.name}`
  }
}

export class PlanningState {
  static Areas = new PlanningState('Area')
  static Processes = new PlanningState('Processes')
  static Machines = new PlanningState('Machines')
  static Configuration = new PlanningState('Configuration')
  static Waiting = new PlanningState('Waiting')
  static Result = new PlanningState('Result')

  constructor(name) {
    this.name = name
  }

  toString() {
    return `PlanningState.${this.name}`
  }

  is(state) {
    return this.name == state.name
  }
}

export function save_and_progress(route, data, planningStore, target) {
  fetch(`http://localhost:5000/${route}`, {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    }
  }).then(planningStore.setState(target))
}
