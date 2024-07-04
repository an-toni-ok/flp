area_properties = {       
    "x_position": { "type": "number"},
    "y_position": { "type": "number"},
    "x_dimension": { "type": "number"},
    "y_dimension": { "type": "number"}
}

area_required_properties = [
    "x_position", 
    "y_position", 
    "x_dimension", 
    "y_dimension"
]

areas = {
    "type": "object",
    "properties": {
        "areas": {
            "type": "array",
            "minItems": 1,
            "items": {
                "properties": area_properties,
                "required": area_required_properties,
                "additionalProperties": False
            }
        },
        "restricted_areas": {
            "type": "array",
            "minItems": 0,
            "items": {
                "properties": area_properties,
                "required": area_required_properties,
                "additionalProperties": False
            }
        }
    },
    "additionalProperties": False
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
        },
        "required": [ 
            "technology", 
            "work_content", 
            "machine_time" 
        ],
        "additionalProperties": False
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
                "minItems": 1,
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
        },
        "required": [
            "name",
            "technologies",
            "hourly_rate",
            "investment_cost",
            "additional_machine_time",
            "x_position",
            "y_position",
            "x_dimension",
            "y_dimension",
            "rotation",
        ],
        "additionalProperties": False
    }
}

objectives = {
    "type": "object",
    "properties": {
        "objectives": {
            "type": "object",
            "properties": {
                "invest": { "type": "boolean" },
                "cost_per_part": { "type": "boolean" },
                "used_area": { "type": "boolean" },
                "number_operators": { "type": "boolean" }
            }
        },
        "target_cycle_time": { "type": "number" },
        "hourly_operator_cost": { "type": "number" }
    },
    "required": [
        "invest",
        "cost_per_part",
        "used_area",
        "number_operators",
        "target_cycle_time",
        "hourly_operator_cost"
    ],
    "additionalProperties": False
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
