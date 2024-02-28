import { defineStore } from 'pinia';

export const useServerStore = defineStore("server", () => {
    const URI = 'http://localhost:5001';
    const PLANNING_DATA_PATH = URI + '/planning-data'
    const START_SESSION_PATH = URI + '/start-session';
    const CANCEL_PATH = URI + '/cancel';

    const mapAreas = (areas) => {
        return areas.map((row) => {
            return {
                x_position: row.x,
                y_position: row.y,
                x_dimension: row.width,
                y_dimension: row.height,
            };
        });
    };

    const mapProductionSteps = (productionSteps) => {
        return productionSteps.map((row) => {
            return {
                technology: row.technology,
                work_content: row.manualTime,
                machine_time: row.machineTime,
            };
        });
    };

    const mapMachines = (machines) => {
        return machines.map((row) => {
            let returnObj = {
                name: row.machineType,
                technologies: row.technologies,
                hourly_rate: row.hourlyMachineCost,
                investment_cost: row.investmentCost,
                additional_machine_time: row.additionalTime,
                x_dimension: row.width,
                y_dimension: row.height,
            };

            if(row.x !== undefined) {
                returnObj.x_position = row.x;
                returnObj.y_position = row.y;
            }
            return returnObj;
        });
    };

    const mapOutputMachines = (machines) => {
        return machines.map((row) => {
            return {
                machineType: row.name,
                id: row.id,
                productionSteps: row.production_steps,
                x: row.x_position,
                y: row.y_position,
                rotation: row.rotation,
                machineTime: row.machine_time,
                workContent: row.work_content,
                cycleTime: row.cycle_time,
                operator: row.assigned_operator,
            };
        });
    };

    const mapObjectives = (objectives) => {
        return {
            invest: objectives.investment,
            cost_per_part: objectives.unitCosts,
            used_area: objectives.spaceConsumption,
            number_operators: objectives.numberOfWorkers,
        };
    };

    const mapOutputObjectives = (objectives) => {
        return {
            investment: objectives.invest,
            unitCosts: objectives.cost_per_part,
            spaceConsumption: objectives.used_area,
            numberOfWorkers: objectives.number_operators,
        };
    };

    const mapOutputOperators = (operators) => {
        return operators.map((row) => {
            return {
                machines: row.assigned_machines,
                workContent: row.work_content,
                cycleTime: row.cycle_time
            };
        });
    };

    return {
        PLANNING_DATA_PATH,
        START_SESSION_PATH,
        CANCEL_PATH,
        mapAreas,
        mapProductionSteps,
        mapMachines,
        mapOutputMachines,
        mapObjectives,
        mapOutputMachines,
        mapOutputObjectives,
        mapOutputOperators,
    };
});