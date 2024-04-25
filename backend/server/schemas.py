area_properties = {       
    "x_position": { "type": "number"},
    "y_position": { "type": "number"},
    "x_dimension": { "type": "number"},
    "y_dimension": { "type": "number"}
}

areas = {
    "type": "object",
    "properties": {
        "area": {
            "type": "array",
            "minItems": 1,
            "properties": area_properties
        },
        "restricted_area": {
            "type": "array",
            "minItems": 0,
            "properties": area_properties
        }
    }
}

production_steps = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "properties": {
            "technology": { "type": "string" },
            "work_content": { "type": "number" },
            "machine_time": { "type": "string" },
        }
    }
}

machines = {
    "type": "array",
    "minItems": 1,
    "items": {
        "type": "object",
        "properties": {
            "name": { "type": "string" },
            "technologies": { 
                "type": "array",
                "items": { "type": "string" }
            },
            "hourly_rate": { "type": "number" },
            "investment_cost": { "type": "number" },
            "additional_machine_time": { "type": "number" },
            "x_position": { "type": "number" },
            "y_position": { "type": "number" },
            "x_dimension": { "type": "number" },
            "y_dimension": { "type": "number" },
            "rotation": { "type": "integer" },
        }
    }
}

objectives = {
    "type": "object",
    "properties": {
        "invest": { "type": "boolean" },
        "cost_per_part": { "type": "boolean" },
        "used_area": { "type": "boolean" },
        "number_operators": { "type": "boolean" },
        "target_cycle_time": { "type": "number" },
        "hourly_operator_cost": { "type": "number" }
    }
}

class SCHEMA:
    """The different JSON schemas for the endpoints.

    Schemas:
        - AREAS
        - PRODUCTION_STEPS
        - MACHINES
        - OBJECTIVES
    """
    AREAS = areas
    PRODUCTION_STEPS = production_steps
    MACHINES = machines
    OBJECTIVES = objectives
