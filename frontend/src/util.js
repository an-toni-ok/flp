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
