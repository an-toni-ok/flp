# Definition of digital twins for operator, sequence, machine, areas and production line

import math
import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class MStep:
    technology: str
    order: int
    work_content: int
    machine_time: int

    def __repr__(self):
        """
        :return: Class representation
        """
        return f"{self.__class__.__name__} (order='{self.order}')"

@dataclass
class MachineType:
    """
    Class for a machine in the production system
    """
    name: str
    technologies: list
    hourly_rate: float
    investment_cost: float
    additional_machine_time: float
    x_dimension: float
    y_dimension: float

    def __repr__(self):
        """
        :return: Class representation
        """
        return f"{self.__class__.__name__} (type='{self.name}')"

@dataclass
class Machine:
    """
    Class for a specific machine
    """
    name: str
    id: int
    type: object
    x_position: float = 0.
    y_position: float = 0.
    rotation: float = 0.
    mstep_list: list = None
    operator: object = None
    machine_time: float = 0.
    work_content: float = 0.
    cycle_time: float = 0.
    
    def _sum_work_content(self) -> float:
        """
        Calculate the work content of the operator.
        :return: operator work content for this station in seconds
        """
        return round(sum([step.work_content for step in self.mstep_list]), 2)

    def _sum_machine_time(self) -> float:
        """
        Calculate the machine/process time for all the productions steps
        :return: machine/process time of station in seconds
        """
        return round(sum([step.machine_time for step in self.mstep_list]), 2)
    
    def calc_cycle_time(self) -> float:
        self.work_content = self._sum_work_content()
        self.machine_time = self._sum_machine_time()
        self.cycle_time = self.work_content + self.machine_time + self.type.additional_machine_time
        return self.cycle_time

    def __repr__(self):
        """
        :return: Class representation
        """
        return f"{self.__class__.__name__} (id='{self.id}')"


@dataclass
class Operator:
    """
    Class for line operator.
    """
    id: int
    hourly_cost: float
    walking_speed: float = 1.
    machine_list: list = None
    work_content: float = 0.
    cycle_time: float = 0.

    def _calc_waypoints(self):
        """
        Calculation of the coordinates of the workplaces of the served machines
        """
        self.waypoint_list = [(m.x_position, m.y_position) for m in self.machine_list]

    def _calc_walking_time(self, distance: float) -> float:
        """
        Calculation of the walking time based on the distance and speed
        :return: walking time in seconds
        """
        return round(distance / self.walking_speed, 2)

    def _sum_walking_time(self) -> float:
        """
        Calculation of the overall walking time for one round trip 
        :return: overall walking time in seconds
        """
        self.waypoint_times = []
        self._calc_waypoints()
        for i, position in enumerate(self.waypoint_list):
            if 0 == i:
                p1 = np.asarray(self.waypoint_list[-1])
            else:
                p1 = np.asarray(self.waypoint_list[i - 1])
            self.waypoint_times.append(self._calc_walking_time(np.linalg.norm(position
                                                                              - p1)))
        self.walking_time = round(sum(self.waypoint_times), 2)
        return self.walking_time

    def _sum_work_content(self) -> float:
        """
        Calculation of the work content (loading and unloading)
        :return: work content in seconds
        """
        self.work_content = round(sum([m.sum_work_content() for m 
                                       in self.machine_list]), 2)
        return self.work_content

    def calc_cycle_time(self) -> float:
        """
        Calculation of the cycle time
        :return: cycle time in seconds
        """
        self.work_content = self._sum_work_content()
        self.walking_time = self._sum_walking_time()
        self.cycle_time = round(self.work_content + self.walking_time, 1)
        return self.cycle_time

    def __repr__(self):
        """
        :return: Class representation
        """
        return f"{self.__class__.__name__} (id='{self.id}')"


@dataclass
class ProductionSystem():
    """
    Class for the whole production system
    """
    target_cycle_time: float 
    objectives: list
    areas: list
    restricted_areas: list
    machine_list: list = None
    operator_list: list = None
    cycle_time: float = 0.
    investment_cost: float = 0.
    cost_per_part: float = 0.
    used_area: float = 0.
    number_operators: int = 0
    x_dimension: float = 0.
    y_dimension: float = 0.

    def _calc_cycle_time(self) -> float:
        """
        Calculation of system cycle time
        :return: system cycle time in seconds
        """
        return round(max([m.calc_cycle_time() for m in self.machine_list]
                         + [o.calc_cycle_time() for o in self.operator_list]), 1)

    def _calc_invest(self) -> int:
        """
        Calculation of investment cost
        :return invest in €
        """
        return round(sum([m.type.investment_cost for m in self.machine_list]), 2)

    def _calc_cost_per_part(self) -> float:
        operator_cost = sum([o.hourly_cost / 3600 * self.cycle_time 
                             for o in self.operator_list])
        machine_cost = sum([m.type.hourly_rate / 3600 * self.cycle_time 
                             for m in self.machine_list])
        return round(operator_cost + machine_cost, 2)

    def _num_operators(self) -> int:
        """
        Get the number of needed operators.
        :return number of operators
        """
        return len(self.operator_list)
    
    def _calc_layout(self) -> None:
        """
        Calculation of the machine positions.

        The machines are split into three line segments (three sides of the U) according to corner indices.
        The length of each line segment is calculated by the sum of the machine widths plus spacing in between.
        The width of each line segment is the maximum machine length within this segment.
        The U-shape is open the right (90 degree clockwise rotation of the U) and the origin for the coordinates is
        the upper right corner with the x-axis going to the left and the y-axis going down.
        """
        positions = []
        rotations = []
        first_line_x = 0
        second_line_y = 0
        third_line_x = 0
        offset = 0.5
        # Calculate x and y dimensions of each segment of the U and calculate local positions
        # First segment
        first_line = self.machine_list[0:self.first_corner]
        for machine in first_line:
            x = machine.type.x_dimension / 2
            positions.append([first_line_x + x])
            rotations.append(0)
            first_line_x += 2*x + offset
        first_line_y = max([machine.type.y_dimension for machine in first_line],
                           default=0)
        # Second segment
        second_line = self.machine_list[self.first_corner:self.second_corner]
        for machine in second_line:
            y = machine.type.x_dimension / 2
            positions.append([second_line_y + y])
            rotations.append(90)
            second_line_y += 2*y + offset
        second_line_x = max([machine.type.y_dimension for machine in second_line], default=0)
        # Third segment
        third_line = self.machine_list[self.second_corner:]
        for machine in third_line:
            x = machine.type.x_dimension / 2
            positions.append([third_line_x + x])
            rotations.append(180)
            third_line_x += 2*x + offset
        third_line_y = max([machine.type.y_dimension for machine in third_line], default=0)
        # Calculate x and y-coordinates of machines in the coordinate system of the whole line. 
        # Origin in right upper corner; U open to the right
        #  ----------X<--.
        # |              |
        # |              Y
        # |
        #  -------------
        positions1 = positions[:self.first_corner]
        positions2 = positions[self.first_corner:self.second_corner]
        positions3 = positions[self.second_corner:]
            
        for position, machine in zip(positions1, first_line):  # first segment
            position[0] = max(first_line_x, third_line_x) - first_line_x + position[0]  # x-coordinate
            position.append(first_line_y - machine.type.x_dimension / 2)  # y-coordinate
        for position, machine in zip(positions2, second_line):  # second segment
            position.append(position[0] + first_line_y + offset) # y-coordinate
            position[0] = max([first_line_x, third_line_x], default=0) + offset + machine.type.y_dimension / 2 # x-coordinate
        for position, machine in zip(positions3, third_line): # third segment
            position[0] = max(first_line_x, third_line_x) - position[0] # x-coordinate
            # y-coordinate
            if second_line_y + offset < 1.7: # ensure a minimum space within the U of 1.7 m
                position.append(first_line_y + 1.7 + machine.type.y_dimension / 2)
            else:
                position.append(first_line_y + second_line_y + 2*offset + machine.type.y_dimension / 2)
        # write coordinates and rotation to machines and stations
        for machine, pos, rot in zip(self.machine_list, positions, rotations):
            machine.x_coordinate = pos[0]
            machine.y_coordinate = pos[1]
            machine.rotation = rot

        # Calculate space requirement
        self.x_dimension = max([first_line_x, third_line_x], default=0) + offset + second_line_x
        if second_line_y + offset < 1.7:
            self.y_dimension = first_line_y + third_line_y + 1.7
        else:
            self.y_dimension = second_line_y + first_line_y + third_line_y + 2*offset

    def evaluate(self) -> None:
        """
        Evalute the system regarding costs restrictions.
        """
        self._calc_layout()
        self.cycle_time = self._calc_cycle_time()
        self.cost_per_part = self._calc_cost_per_part()
        self.investment_cost = self._calc_invest()
        self.number_operators = self._num_operators()

    def _do_operators_cross(self) -> bool:
        """
        Check whether the operator routes cross each other.
        :return: True if operators cross, False otherwise
        """
        def on_segment(p, q, r):
            """
            Given three collinear points p, q, r, the function checks if  
            point q lies on line segment 'pr'.
            :param p: (x, y)-coordinates of point p
            :param q: (x, y)-coordinates of point q
            :param r: (x, y)-coordinates of point r 
            :return: True if q lies on line 'pr', False otherwise
            """
            if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                    (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
                return True
            return False

        def orientation(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> int:
            """
            Find the orientation of an ordered triplet (p,q,r)

            See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
            for details of below formula.

            :param p: (x, y)-coordinates of point p
            :param q: (x, y)-coordinates of point q
            :param r: (x, y)-coordinates of point r 
            :return: 0 if Collinear points; 1 if Clockwise points; 2 if Counterclockwise             
            """
            val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
            if (val > 0):
                # Clockwise orientation 
                return 1
            elif (val < 0):
                # Counterclockwise orientation 
                return 2
            else:
                # Collinear orientation 
                return 0

        def do_intersect(p1, q1, p2, q2):
            """
            Check if line segments 'p1q1' and 'p2q2' intersect.
            :param p1: start point of line segment 1
            :param q1: end point of line segment 1
            :param p2: start point of line segment 2
            :param q2: end point of line segment 2
            :return: True if the two line segments intersect, False otherwise
            """

            # Find the 4 orientations required for  
            # the general and special cases 
            o1 = orientation(p1, q1, p2)
            o2 = orientation(p1, q1, q2)
            o3 = orientation(p2, q2, p1)
            o4 = orientation(p2, q2, q1)

            # General case 
            if ((o1 != o2) and (o3 != o4)):
                return True

            # Special Cases 

            # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
            if ((o1 == 0) and on_segment(p1, p2, q1)):
                return True

            # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
            if ((o2 == 0) and on_segment(p1, q2, q1)):
                return True

            # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
            if ((o3 == 0) and on_segment(p2, p1, q2)):
                return True

            # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
            if ((o4 == 0) and on_segment(p2, q1, q2)):
                return True

            # If none of the cases 
            return False

        def get_path_segments(waypoint_list: list[tuple[float, float]]) -> list[tuple[
                                            tuple[float, float], tuple[float, float]]]:
            """
            Convert operator waypoint list in line segments.
            :param waypoint_list: list of the waypoints of the operator
            :return: list of line segements for this operator
            """
            segments = []
            for i, q in enumerate(waypoint_list):
                if 0 == i:
                    p = waypoint_list[-1]
                else:
                    p = waypoint_list[i - 1]
                segments.append((p, q))
            return segments

        def adjust_endpoints(segment: tuple[tuple[float, float], tuple[float, float]]) -> tuple[
                                                        tuple[float, float], tuple[float, float]]:
            """
            Slightly shorten the line segment on both ends to avoid two segments being flagged as intersecting
            when one segments ends on the other segment.
            :param segment: start and end point of the line segment
            :return: shortened line segment
            """
            p, q = segment
            new_p = ((q[0] - p[0]) * 0.001, (q[1] - p[1]) * 0.001)
            new_q = ((p[0] - q[0]) * 0.001, (p[1] - q[1]) * 0.001)
            return (new_p, new_q)

        # iterate through all combinations of operators and their line segments to check for any intersection
        for i, operator1 in enumerate(self.operator_list):
            segments1 = get_path_segments(operator1.waypoint_list)
            for operator2 in self.operator_list[i:]:
                segments2 = get_path_segments(operator2.waypoint_list)
                for segment1 in segments1:
                    for segment2 in segments2:
                        adjusted_segment1 = adjust_endpoints(segment1)
                        if do_intersect(*adjusted_segment1, *segment2):
                            return True
                        adjusted_segment2 = adjust_endpoints(segment2)
                        if do_intersect(*segment1, *adjusted_segment2):
                            return True
        return False
    
    def _check_validity(self) -> bool:
        """
        Check if all restrictions for the line are met.
        :return: True if all restrictions are fulfilled, False otherwise
        """
        if self.space_requirement > 0.:
            return False
        if self.excess_payload > 0.:
            return False
        if self.ergonomics > 0.:
            return False
        if self.crossing_operators:
            return False
        if self.cycle_time > self.plant.target_cycle_time:
            return False
        return True