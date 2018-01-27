"""
Can be used to validate and score your solution
Usage: validate.py <file name>
"""

import sys
import math
import pandas as pd


MAX_DELIVERIES = 10
DRIVE_SPEED_KMPH = 20
PRICE_PER_TRUCK = 100
PRICE_PER_KM = 0.061

def distance(pos1, pos2):
    """Find the euclidean distance between two, two dimentional tuples"""
    diff_1 = pos1[0] - pos2[0]
    diff_2 = pos1[1] - pos2[1]
    return math.sqrt(diff_1*diff_1 + diff_2*diff_2)


def is_valid(data_frame):
    """Check if the route provided for a truck is legal.
       Print any problems to stderr"""
    epsilon = 0.00001
    check = data_frame.copy()
    check.sort_values("sequence_number", inplace=True)
    location = (0, 0)
    time = 0
    valid = []
    # Check all deliveries make their time windows
    row = ""
    for _, row in check.iterrows():
        new_location = (row.x, row.y)
        travel_time_hours = distance(location, new_location) / DRIVE_SPEED_KMPH
        time = time + travel_time_hours
        if time > row.time_window_start+1:
            sys.stderr.write("Error: Truck " + str(row.truck_id)
                             + " delivers to " + str(row.order_id)
                             + " late at " + str(time) + "\n")
            valid.append(False)
        else:
            valid.append(True)
        if time - epsilon < row.time_window_start:
            time = row.time_window_start
        location = new_location

    # Check the van returns to the depot in time
    new_location = (0, 0)
    travel_time_hours = distance(location, new_location) / DRIVE_SPEED_KMPH
    time = time + travel_time_hours
    if time - epsilon > 10:
        sys.stderr.write("Error: Truck " + str(row.truck_id)
                         + " returns to the depot at " + str(time) + "\n")
        valid = [False] * len(check)

    # Check the van makes at most 10 deliveries
    if len(check) > MAX_DELIVERIES:
        sys.stderr.write("Error: Truck " + str(row.truck_id)
                         + " delivers to " + str(len(check)) + " orders.\n")
        valid = [False] * len(check)
    return valid


def route_distance(data_frame):
    """Check if the route provided for a truck is legal.
       Print any problems to stderr"""
    check = data_frame.copy()
    check.sort_values("sequence_number", inplace=True)
    location = (0, 0)
    total_distance = 0
    # Sum the distances to last order
    for _, row in check.iterrows():
        new_location = (row.x, row.y)
        total_distance += distance(location, new_location)
        location = new_location

    # Add distance to depot
    new_location = (0, 0)
    total_distance += distance(location, new_location)

    return total_distance


def main(file_name):
    """
    Find the score for the solution and report any problems
    """
    # Columns are: truck_id, order_id, sequence_number
    data = pd.read_csv(file_name)
    data.columns = [column.strip() for column in data.columns.tolist()]
    # Columns are: order_id, x, y, time_window_start
    orders = pd.read_csv("orders.csv")
    orders.columns = [column.strip() for column in orders.columns.tolist()]
    data = data.merge(orders, on="order_id")

    # Check correct unique orders
    specified_orders = data.order_id.nunique()
    if specified_orders != len(orders):
        sys.stderr.write("Error: " + str(specified_orders) + " specified. "
                         + str(len(orders)) + " orders required.\n")
        exit(1)

    # Check specified duplicate orders
    duplicates = data.order_id.duplicated()
    if sum(duplicates):
        msg = "Error: the following order(s) have multiple deliveries:\n"
        duplicated_orders = data[duplicates].groupby("order_id")
        duplicated_orders = duplicated_orders.mean().reset_index().order_id
        duplicated_orders = duplicated_orders.values.tolist()
        sys.stderr.write(msg + str(duplicated_orders) + "\n")
        exit(1)

    # Check the validity of the routes
    valid = data.groupby("truck_id").apply(is_valid).tolist()
    valid = [x for sublist in valid for x in sublist]
    total_distance = sum(data.groupby("truck_id").apply(route_distance))

    if not sum(valid) == len(data):
        print("Invalid solution")
        exit(1)
    else:
        vans = data.truck_id.nunique()
        print("Correct solution found with "
              + str(vans) + " trucks.")
        print("Total distance travelled: {0:.2f}".format(total_distance)
              + " km")
        cost = vans*100 + total_distance*0.061
        print("Total cost: £{0:.2f}".format(cost))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: validate.py <file name>\n")
        exit(1)

    main(sys.argv[1])
