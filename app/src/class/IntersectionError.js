class IntersectionError extends Error {
    constructor(areaType) {
      super(areaType + " würden sich überschneiden!");
      this.name = "IntersectionError";
    };
};

export default IntersectionError;