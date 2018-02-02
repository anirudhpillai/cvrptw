# ICHack 18
We won the Ocado technology challenge by building the most optimal solution
to the Capacitated Vehicle Routing Problem with Time Windows at the Hackathon.
Below are the details of the problem.

Our approach is outlined in the Jupyter notebook and the code is in `answer.py`.

## Problem Spec

### Rules

The problem is to minimise the cost of servicing orders with a fleet of trucks.

Trucks can only service 10 orders. Driving takes 1 hour per 20 km. A day lasts 10 hours. All trucks start at the beginning of the day (hour 0) and must return before the end (hour 10). Using a truck costs £100 and the price of fuel per km is 6.1p.

Trucks must deliver in the order's time window. Times windows start on the hour and last one hour. Trucks may arrive early and wait until the time window begins before delivering. For simplicity delivery is instant.

### Data

Provided data comes in four columns:
orderi\_id uniquely identifies the order.
x and y describe the relative location to the depot (at 0, 0) in Cartesian coordinates.
time\_window\_start gives the start time (in hours) we can deliver from. So delivery is not permitted after time\_window\_start+1
To validate your solution data needs to be provided with these columns:
truck\_id - uniquely identify the truck that will make an order
order\_id - the order\_id from orders.csv the truck should drive to
sequence\_number - the stage in the trucks journey it should travel to this order (i.e. 1 for the first order, 2 for the second order, etc.)

### Validation

Running the provided script requires python3 with pandas

To validate your solution simply call:

`python validate.py <filename>`

The script assumes orders.csv is in the same directory. If it breaks, ensure that is the case.

An intentionally poorly performing example submission has been provided.    
