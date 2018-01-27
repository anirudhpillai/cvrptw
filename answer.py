import csv
import math
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np



MAX_DELIVERIES = 10
DRIVE_SPEED_KMPH = 20
PRICE_PER_TRUCK = 100
PRICE_PER_KM = 0.061
MAX_TIME_PER_TRUCK = 10

TOTAL_CLUSTERS = 70


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


class Truck:
    id = 0

    def __init__(self):
        self.capacity_left = MAX_DELIVERIES
        self.x = 0
        self.y = 0
        self.current_time = 0
        self.id = Truck.id
        self.deliveries = []  # [truck_id, order_id, seq_no]
        self.current_order = 1
        Truck.id += 1

    def can_deliver_order(self, order):
        """
        Checks whether the truck can deliver the order and reach the depot in
        time.
        """
        if self.capacity_left == 0:
            return False

        time_to_reach_order = distance(self.x, self.y, order.x, order.y) / DRIVE_SPEED_KMPH

        if self.current_time + time_to_reach_order >= order.end_time:
            return False

        time_to_reach_depot = distance(order.x, order.y, 0, 0) / DRIVE_SPEED_KMPH

        if (
            max(self.current_time + time_to_reach_order, order.start_time)
                + time_to_reach_depot > MAX_TIME_PER_TRUCK
        ):
            return False

        print("True")
        return True

    def deliver_order(self, order):
        dist = distance(self.x, self.y, order.x, order.y)

        # update current_time
        self.current_time = max(
            self.current_time + (dist / DRIVE_SPEED_KMPH),
            order.start_time
        )

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
        if current_truck.can_deliver_order(top):
            current_truck.deliver_order(top)
        else:
            deliveries.extend(current_truck.deliveries[::])
            current_truck = Truck()
            current_truck.deliver_order(top)

    if len(deliveries) < 500:
        deliveries.extend(current_truck.deliveries[::])

    return deliveries


def clustered(orders, kmeans):
    clusters = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
    deliveries = []

    # loop over each cluster
    for cluster in clusters.values():
        curr_len = len(deliveries)
        current_truck = Truck()

        for idx in cluster:
            order = orders[idx]
            if current_truck.can_deliver_order(order):
                current_truck.deliver_order(order)
            else:
                deliveries.extend(current_truck.deliveries[::])
                current_truck = Truck()
                current_truck.deliver_order(order)

        if len(deliveries) - curr_len < len(cluster):
            deliveries.extend(current_truck.deliveries[::])

    return deliveries


def answer():
    df = pd.read_csv("orders.csv")

    orders_to_cluster = []
    orders = []

    for _, row in df.iterrows():
        orders_to_cluster.append([row["x"], row["y"]])
        order = Order(
            row["order_id"], row["x"], row["y"], row["time_window_start"]
        )
        orders.append(order)

    kmeans = KMeans(n_clusters=TOTAL_CLUSTERS, random_state=0)
    kmeans.fit(orders_to_cluster)

    print(len(orders))

    # ans_list = bruteforce(orders)
    ans_list = clustered(orders, kmeans)

    print(len(ans_list))

    with open("answer.txt", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["truck_id", "order_id", "sequence_number"])
        for row in ans_list:
            writer.writerow(row)


answer()
