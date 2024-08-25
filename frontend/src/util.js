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

export class RunStatus {
  constructor(status) {
    this.state = undefined
    switch (status) {
      case 'INPUT':
        this.state = 'Eingabe'
        break
      case 'RUNNING':
        this.state = 'Laufend'
        break
      case 'COMPLETED':
        this.state = 'Abgeschlossen'
        break
      case 'ERROR':
        this.state = 'Fehler'
        break
    }
  }

  toString() {
    return `${this.state}`
  }
}

export function post_request(route, data) {
  let request_data = {
    method: 'POST',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    }
  }
  if (data !== undefined) {
    request_data.body = JSON.stringify(data)
  }

  return fetch(`${route}`, request_data)
}

export function get_request(route) {
  return fetch(`${route}`, {
    method: 'GET',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    }
  })
}
