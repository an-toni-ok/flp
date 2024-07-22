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

export class PlanningState {
  static Areas = new PlanningState('Area')
  static Processes = new PlanningState('Processes')
  static Machines = new PlanningState('Machines')
  static Configuration = new PlanningState('Configuration')
  static Overview = new PlanningState('Overview')

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
