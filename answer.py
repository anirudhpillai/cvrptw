import csv
import math
import pandas as pd


MAX_DELIVERIES = 10
DRIVE_SPEED_KMPH = 20
PRICE_PER_TRUCK = 100
PRICE_PER_KM = 0.061
MAX_TIME_PER_TRUCK = 10


def distance(x1, x2, y1, y2):
    return math.sqrt(abs(x1 - x2) + abs(y1 - y2))


# class Graph:
#     def __init__(self, orders):
#         self.matrix = {}
#
#         for o1 in orders:
#             self.matrix[o1.id] = {}
#
#             for o2 in orders:
#                 self.matrix[o1.id][o2.id] = distance(
#                     o1.x, o1.y, o2.x, o2.y
#                 )


class Truck:
    id = 0

    def __init__(self):
        self.capacity_left = MAX_DELIVERIES
        # self.distance_travelled = 0
        self.x = 0
        self.y = 0
        self.current_time = 0
        self.id = Truck.id
        self.deliveries = []  # [truck_id, order_id, seq_no]
        self.current_order = 1
        Truck.id += 1

    def has_capacity(self):
        return self.capacity_left > 0

    def can_deliver_order(self, order):
        """
        Checks whether the truck can deliver the order and reach the depot in
        time.
        """
        time_to_reach_order = distance(self.x, self.y, order.x, order.y)
        if self.current_time + time_to_reach_order > order.end_time:
            return False

        time_to_reach_depot = distance(order.x, order.y, 0, 0) / DRIVE_SPEED_KMPH
        if (self.current_time + time_to_reach_order
                + time_to_reach_depot > MAX_TIME_PER_TRUCK):
            return False

        return True

    def deliver_order(self, order):
        dist = distance(self.x, self.y, order.x, order.y)
        # self.distance_travelled += dist

        # update current_time
        self.current_time += max(dist / DRIVE_SPEED_KMPH, order.start_time)

        # update capacity
        self.capacity_left -= 1

        # update location
        self.x = order.x
        self.y = order.y

        # add order to deliveries
        self.deliveries.append([self.id, order.id, self.current_order])
        self.current_order += 1


class Order:
    def __init__(self, id, x, y, start_time):
        self.id = id
        self.x = x
        self.y = y
        self.start_time = start_time
        self.end_time = self.start_time + 1


def bruteforce(orders):
    deliveries = []
    current_truck = Truck()

    while orders:
        top = orders.pop()
        if current_truck.has_capacity() and current_truck.can_deliver_order(top):
            current_truck.deliver_order(top)
        else:
            deliveries.extend(current_truck.deliveries[::])
            current_truck = Truck()
            current_truck.deliver_order(top)

    if len(deliveries) < 500:
        deliveries.extend(current_truck.deliveries[::])

    return deliveries


def answer():
    # Columns are: order_id, x, y time_window_start
    df = pd.read_csv("orders.csv")

    orders = []
    for _, row in df.iterrows():
        orders.append(Order(
            row["order_id"], row["x"], row["y"], row["time_window_start"]
        ))

    print(len(orders))

    ans_list = bruteforce(orders)

    print(len(ans_list))

    with open("answer.txt", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in ans_list:
            # writer.writerow("%d, %d, %d" % (t_id, o_id, s_no))
            writer.writerow(row)

    # graph = Graph(orders)
    # print(graph.matrix)

    # write answer to file
    # orders.to_csv("answer.txt")


answer()
