import json
import uuid

# Simulate optimization script
def calculate(data):
    input = json.loads(data)

    outputObj = {
                'technologies': input['technologies'],
                'machines': [],
                'operators': [],
                'objectives': {},
    }

    for index, machine in enumerate(input['machines']):
        output_machine = {}
        output_machine['name'] = machine['name']
        output_machine['id'] = index
        output_machine['production_steps'] = []
        output_machine['x_position'] = machine['x_position']
        output_machine['y_position'] = machine['y_position']
        output_machine['rotation'] = 0
        output_machine['machine_time'] = 50
        output_machine['work_content'] = 24
        output_machine['cycle_time'] = 74
        output_machine['assigned_operator'] = 1
        outputObj['machines'].append(output_machine)
        for stepindex, step in enumerate(input['production_steps']):
            for technology in machine['technologies']:
                if step['technology'] == technology:
                    output_machine['production_steps'].append(stepindex)

    operator = {
        'assigned_machines': [0, 1, 2],
        'work_content': 28,
        'cycle_time': 600
    }
    outputObj['operators'].append(operator)

    if input['objectives']['invest']:
        outputObj['objectives']['invest'] = 300000
    else:
        outputObj['objectives']['invest'] = 600000

    if input['objectives']['cost_per_part']:
        outputObj['objectives']['cost_per_part'] = 220
    else:
        outputObj['objectives']['cost_per_part'] = 300

    if input['objectives']['used_area']:
        outputObj['objectives']['used_area'] = 3000
    else:
        outputObj['objectives']['used_area'] = 5000

    if input['objectives']['number_operators']:
        outputObj['objectives']['number_operators'] = 2
    else:
        outputObj['objectives']['number_operators'] = 3

    outputObj['line_cycle_time'] = 2000

    outputObj = json.dumps(outputObj)

    return outputObj