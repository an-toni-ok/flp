class OutOfBoundsError extends Error {
    constructor(areaType) {
        super(areaType + " wäre außerhalb ihrer Grenzen!");
        this.name = "OutOfBoundsError";
    };
};

export default OutOfBoundsError;