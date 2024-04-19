from flask import Flask, request, jsonify, json, make_response, session
from flask_cors import CORS
from flask_session import Session
import calc
import calc2
import sqlite3
import time

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_COOKIE_SAMESITE'] = None
Session(app)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

progress = {}
cancel = {}

# set session id and send cookie to browser
@app.route('/start-session', methods=['GET'])
def start_session():
    global cancel
    global progress
    res = make_response("")
    progress[session.sid] = 0
    cancel[session.sid] = False
    res.set_cookie('session', session.sid, samesite='None', secure=True)
    return (res)


# planning data route
@app.route('/planning-data', methods=['GET', 'POST', 'OPTIONS'])
def data_processing():
    global progress
    global cancel
    # start optimization with uploaded data,
    # when done return results to the frontend
    if request.method == 'POST':
        session_id = session.sid
        progress[session_id] = 0
        cancel[session_id] = False
        response_object = {}
        post_data = request.get_json()
        input_data = json.dumps(post_data)
        is_edited = 'line_id' in post_data.keys()

        # Simulate processing time
        processing_time = 100
        if not is_edited:
            for i in range(processing_time):
                # Cancel processing if user clicks cancel button in frontend
                if cancel[session_id]:
                    res = make_response(response_object)
                  
                    return res
                time.sleep (0.1)
                if(i % (processing_time/100) == 0):
                    progress[session_id] += 1
        
        # Simulate optimization script and put output data into the response object
        output_data = json.loads(run_script(input_data))
        response_object['output_data'] = output_data
        
        # insert line data into database
        line_data = {'target_cycle_time': post_data['target_cycle_time'],
                     'hourly_operator_cost': post_data['hourly_operator_cost'],
                     'production_steps': post_data['production_steps'],
                     'areas': post_data['areas'],
                     'restricted_areas': post_data['restricted_areas'],
                     'input_machines': post_data['machines'],
                     'output_data': output_data
                     }
        
        if is_edited:
            line_data['output_data']['is_edited'] = True
            insert_layout_data(line_data, post_data['line_id'])
        else: 
            line_id = insert_line_data(line_data)
            response_object['line_id'] = line_id

        if not is_edited:
            time.sleep(1)

        res = make_response(response_object)
        return res
    
    # return current progress
    if request.method == 'GET':
        res = make_response({'progress': progress[session.sid]})
        return res
    
    if request.method == 'OPTIONS':
        res = make_response("")
        return res
    

# route for canceling the current optimization process
@app.route('/cancel', methods=['GET'])
def cancel_script():
    global cancel
    res = make_response("")
    cancel[session.sid] = True
    return res


def run_script(data):
    # run script for edited layout when line_id is defined
    if 'line_id' in json.loads(data).keys():
        return calc2.calculate(data)
    else:
        return calc.calculate(data)


# insert line data into the database
def insert_line_data(data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO line (" +
                    "target_cycle_time, " +
                    "hourly_operator_cost) " +
                    "VALUES (?, ?);",
            (data['target_cycle_time'],
             data['hourly_operator_cost']
            )
        )

        line_id = cur.lastrowid

        for index, step in enumerate(data['production_steps']):
            cur.execute("INSERT INTO production_step (" +
                        "line_id, " +
                        "id, " +
                        "technology, " +
                        "machine_time, " +
                        "work_content) " +
                        "VALUES (?, ?, ?, ?, ?);",
                (line_id,
                 index, 
                 step['technology'],
                 step['machine_time'],
                 step['work_content']
                )
            )

        for area in data['areas']:
            cur.execute("INSERT INTO area (" +
                        "line_id, " +
                        "x_dimension, " +
                        "y_dimension, " +
                        "x_position, " +
                        "y_position) " +
                        "VALUES (?, ?, ?, ?, ?);",
                (line_id,
                 area['x_dimension'], 
                 area['y_dimension'],
                 area['x_position'],
                 area['y_position']
                )
            )

        for area in data['restricted_areas']:
            cur.execute("INSERT INTO restricted_area (" +
                        "line_id, " +
                        "x_dimension, " +
                        "y_dimension, " +
                        "x_position, " +
                        "y_position) " +
                        "VALUES (?, ?, ?, ?, ?);",
                (line_id,
                 area['x_dimension'], 
                 area['y_dimension'],
                 area['x_position'],
                 area['y_position']
                )
            )

        for layout in data['output_data']:
            cur.execute("INSERT INTO layout (" + 
                        "line_id, " +
                        "cycle_time, " +
                        "investment_cost, " +
                        "cost_per_part, " +
                        "used_area, " +
                        "number_operators) " +
                        "VALUES (?, ?, ?, ?, ?, ?);",
                (line_id,
                 layout['line_cycle_time'],
                 layout['objectives']['invest'],
                 layout['objectives']['cost_per_part'],
                 layout['objectives']['used_area'],
                 layout['objectives']['number_operators'],
                )
            )

            layout_id = cur.lastrowid

            for index, operator in enumerate(layout['operators']):
                cur.execute("INSERT INTO operator (" + 
                            "layout_id, " +
                            "id, " +
                            "work_content, " +
                            "cycle_time) " +
                            "VALUES (?, ?, ?, ?);",
                    (layout_id,
                    index, 
                    operator['work_content'],
                    operator['cycle_time'],
                    )
                )

            for index, machine in enumerate(layout['machines']):
                production_steps = json.dumps(machine['production_steps'])
                cur.execute("INSERT INTO machine (" +
                            "layout_id, " +
                            "id, " +
                            "name, " +
                            "x_dimension, " +
                            "y_dimension, " +
                            "x_position, " +
                            "y_position, " +
                            "rotation, " +
                            "machine_time, " +
                            "work_content, " +
                            "cycle_time, " +
                            "operator_id, " +
                            "production_steps) " +
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    (layout_id,
                    machine['id'], 
                    machine['name'],
                    data['input_machines'][index]['x_dimension'],
                    data['input_machines'][index]['y_dimension'],
                    machine['x_position'],
                     machine['y_position'],
                     machine['rotation'],
                     machine['machine_time'],
                     machine['work_content'],
                     machine['cycle_time'],
                     machine['assigned_operator'],
                     production_steps,
                    )
                )

        conn.commit()
    except Exception as err:
         print(err)
         conn.rollback()
    finally:
         conn.close()
         return line_id
    
# insert layout data into database
def insert_layout_data(data, line_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        layout = data['output_data']
        is_edited = 0

        if layout['is_edited']:
            is_edited = 1

        cur.execute("INSERT INTO layout (" + 
                    "line_id, " +
                    "cycle_time, " +
                    "investment_cost, " +
                    "cost_per_part, " +
                    "used_area, " +
                    "number_operators, " +
                    "is_edited) " +
                    "VALUES (?, ?, ?, ?, ?, ?, ?);",
            (line_id,
             layout['line_cycle_time'],
             layout['objectives']['invest'],
             layout['objectives']['cost_per_part'],
             layout['objectives']['used_area'],
             layout['objectives']['number_operators'],
             is_edited
            )
        )

        layout_id = cur.lastrowid

        for index, operator in enumerate(layout['operators']):
            cur.execute("INSERT INTO operator (" + 
                        "layout_id, " +
                        "id, " +
                        "work_content, " +
                        "cycle_time) " +
                        "VALUES (?, ?, ?, ?);",
                (layout_id,
                index, 
                operator['work_content'],
                operator['cycle_time'],
                )
            )

        for index, machine in enumerate(layout['machines']):
            production_steps = json.dumps(machine['production_steps'])
            cur.execute("INSERT INTO machine (" +
                        "layout_id, " +
                        "id, " +
                        "name, " +
                        "x_dimension, " +
                        "y_dimension, " +
                        "x_position, " +
                        "y_position, " +
                        "rotation, " +
                        "machine_time, " +
                        "work_content, " +
                        "cycle_time, " +
                        "operator_id, " +
                        "production_steps) " +
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (layout_id,
                machine['id'], 
                machine['name'],
                data['input_machines'][index]['x_dimension'],
                data['input_machines'][index]['y_dimension'],
                machine['x_position'],
                 machine['y_position'],
                 machine['rotation'],
                 machine['machine_time'],
                 machine['work_content'],
                 machine['cycle_time'],
                 machine['assigned_operator'],
                 production_steps,
                )
            )

        conn.commit()
    except Exception as err:
         print(err)
         conn.rollback()
    finally:
         conn.close()


# get database connection
def get_db_connection():
    conn = sqlite3.connect('FLP@THA.db')
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)