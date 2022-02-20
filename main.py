#import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import copy
import math
import time


class Point:
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.color = 10000

    def get_man_dist(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

    def get_euc_dist(self, p):
        return math.sqrt(math.pow(self.x - p.x, 2) + math.pow(self.y - p.y, 2))


class KMeansClustering:
    def __init__(self, k_param):
        self.k_param = k_param
        self.means = []
        self.saveIndex = 0

    def cluster(self):
        k = 0
        while k < self.k_param:
            temp_index = random.randint(0, len(dataset) - 1)
            b_ok = True
            for x in self.means:
                # aby neboli meany prilis blizko seba
                if x.get_euc_dist(dataset[temp_index]) < int(INTERVAL / self.k_param):
                    b_ok = False
            if b_ok is True:
                self.means.append(copy.deepcopy(dataset[temp_index]))
                k += 1

        change = True
        while change is True:

            change = False
            mean_sums = []
            mean_counts = []
            for i in range(self.k_param):
                mean_sums.append(Point(0, 0))
                mean_counts.append(0)

            for point in dataset:
                min_distance = 1000000.0
                min_k = 0
                for k in range(self.k_param):
                    distance = point.get_euc_dist(self.means[k])
                    if distance < min_distance:
                        min_distance = distance
                        min_k = k

                if point.color != min_k * 10:
                    change = True

                mean_sums[min_k].x += point.x
                mean_sums[min_k].y += point.y
                mean_counts[min_k] += 1

                point.color = min_k * 10

            #self.print_img(True)
            #self.saveIndex += 1

            for k in range(self.k_param):
                if mean_counts[k] == 0:
                    mean_counts[k] = 1

                self.means[k].x = mean_sums[k].x / mean_counts[k]
                self.means[k].y = mean_sums[k].y / mean_counts[k]

    def print_img(self, save):
        x_vals, y_vals = zip(*[(int(bod.x), int(bod.y)) for bod in dataset])

        plt.scatter(x_vals, y_vals, c=[point.color for point in dataset])

        for k in range(self.k_param):
            plt.scatter(self.means[k].x, self.means[k].y, c="black", marker="x")

        plt.title("K_mean, k=" + str(self.k_param) + ", pocet bodov=" + str(NUM_POINTS))
        if save:
            plt.savefig("kMean_k" + str(self.k_param) + "_" + str(NUM_POINTS) + "_" + str(GsaveIndex) + ".jpg")
        else:
            plt.show()
        plt.clf()

dataset = []


def check_unique(x, y):
    for p in dataset:
        if p.x == x and p.y == y:
            return False
    return True


def generate_data():
    for i in range(20):
        new_x = random.randint(LBOUND, RBOUND)
        new_y = random.randint(LBOUND, RBOUND)

        if check_unique(new_x, new_y):
            dataset.append(Point(new_x, new_y))
        else:
            i -= 1

    for i in range(NUM_POINTS):
        point = dataset[random.randint(0, len(dataset) - 1)]

        new_x = point.x + random.randint(-100, 100)
        new_y = point.y + random.randint(-100, 100)
        dataset.append(Point(new_x, new_y))


class KMedoidClustering:
    def __init__(self, k_param):
        self.k_param = k_param
        self.medoids = []
        self.medoid_sums = []
        self.clusterIndexes = [{} for i in range(k_param)]
        self.saveIndex = 0

    def cluster(self):
        k = 0
        while k < self.k_param:
            temp_index = random.randint(0, len(dataset) - 1)
            b_ok = True
            for x in self.medoids:
                #aby neboli medoidy prilis blizko seba
                if x.get_man_dist(dataset[temp_index]) < int(INTERVAL / self.k_param):
                    b_ok = False
            if b_ok is True:
                self.medoids.append(copy.deepcopy(dataset[temp_index]))
                k += 1

        change = True
        first_iter = True

        while change is True:

            change = False
            self.medoid_sums = []

            for i in range(self.k_param):
                self.medoid_sums.append(0)
            help_index = 0
            for point in dataset:
                min_distance = 1000000.0
                min_k = 0
                for k in range(self.k_param):
                    distance = point.get_man_dist(self.medoids[k])
                    if distance < min_distance:
                        min_distance = distance
                        min_k = k

                if point.color != min_k * 10:
                    change = True
                    #odstran zo stareho clustra
                    if not first_iter:
                        del self.clusterIndexes[int(point.color / 10)][help_index]

                self.medoid_sums[min_k] += min_distance
                self.clusterIndexes[min_k][help_index] = help_index
                point.color = min_k * 10
                help_index += 1

            self.do_swap()
            #self.print_img(True)
            #self.saveIndex += 1
            first_iter = False

    def do_swap(self):
        for k in range(self.k_param):
            best_i = None
            for index1 in self.clusterIndexes[k]:
                distance = 0
                for index2 in self.clusterIndexes[k]:
                    # ak su rovnake
                    if dataset[index1] == dataset[index2]:
                        continue
                    distance += dataset[index1].get_man_dist(dataset[index2])
                if distance < self.medoid_sums[k]:
                    self.medoid_sums[k] = distance
                    best_i = index1
            # urobim swap
            if best_i is not None:
                self.medoids[k] = copy.deepcopy(dataset[best_i])

    def print_img(self, save):
        x_vals, y_vals = zip(*[(int(bod.x), int(bod.y)) for bod in dataset])

        plt.scatter(x_vals, y_vals, c=[point.color for point in dataset])

        for k in range(self.k_param):
            plt.scatter(self.medoids[k].x, self.medoids[k].y, c="black", marker="x")
        plt.title("K_medoid, k=" + str(self.k_param) + ", pocet bodov=" + str(NUM_POINTS))
        if save:
            plt.savefig("kMedoid_k" + str(self.k_param) + "_" + str(NUM_POINTS) + "_" + str(GsaveIndex) + ".jpg")
        else:
            plt.show()
        plt.clf()


class AgglomerativeClustering:
    def __init__(self, k_param):
        self.k_param = k_param
        self.clusterIndexes = [{} for i in range(len(dataset))]
        self.saveIndex = 0
        self.matrix = [[] for i in range(len(dataset))]

    def cluster(self):
        clusters_num = len(dataset)
        for index in range(len(dataset)):
            self.clusterIndexes[index][index] = index

        index1 = 0
        for p1 in dataset:
            for p2 in dataset:
                if p1 == p2:
                    self.matrix[index1].append(0)
                    break
                self.matrix[index1].append(p1.get_euc_dist(p2))
            index1 += 1

        while clusters_num > self.k_param:
            min_distance = None
            best1 = None
            best2 = None
            index1 = 0
            for c1 in self.clusterIndexes:
                index2 = 0
                for c2 in self.clusterIndexes:
                    if c1 == c2:
                        break

                    distance = self.matrix[index1][index2]
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        best1 = min(index1, index2)
                        best2 = max(index2, index1)
                    index2 += 1
                index1 += 1

            self.join(best1, best2)
            #print(len(self.clusterIndexes))
            clusters_num -= 1

        #zafarbujem body len raz a to na konci algoritmu
        color_index = 0
        for c in self.clusterIndexes:
            for p_index in c:
                dataset[p_index].color = color_index * 10

            color_index += 1

    def join(self, c1, c2):
        #zlucit zoznamy clustrov
        for x in self.clusterIndexes[c2]:
            self.clusterIndexes[c1][x] = x
        self.clusterIndexes.remove(self.clusterIndexes[c2])

        #prepocitat riadok
        col_index = 0
        for hodnota in self.matrix[c1]:
            hodnota = min(self.matrix[c1][col_index], self.matrix[c2][col_index])
            col_index += 1

        #prepocitat stpec
        col_index = c2 - 1
        for row_index in range(c2 - 1, c1):
            self.matrix[row_index][c1] = min(self.matrix[row_index][c1], self.matrix[row_index][col_index])
            col_index -= 1

        # odstran riadok a stlpec druheho
        del self.matrix[c2]
        for row in self.matrix:
            if len(row) > c2:
                del row[c2]

    def print_img(self, save):
        x_vals, y_vals = zip(*[(int(bod.x), int(bod.y)) for bod in dataset])

        plt.scatter(x_vals, y_vals, c=[point.color for point in dataset])

        plt.title("Agglo, k=" + str(self.k_param) + ", pocet bodov=" + str(NUM_POINTS))
        if save:
            plt.savefig("agglo" + str(self.k_param) + "_" + str(NUM_POINTS) + "_" + str(GsaveIndex) + ".jpg")
        else:
            plt.show()
        plt.clf()


class DivisiveClustering:
    def __init__(self, k_param):
        self.k_param = k_param
        self.clusterIndexes = [{}]
        self.finalMeans = []
        self.saveIndex = 0
        self.firstIter = True

    def cluster(self):
        for i in range(len(dataset)):
            self.clusterIndexes[0][i] = i
        i = 1
        max_i = 0
        while i < self.k_param:
            temp_i = 0
            max_len = 0
            for c in self.clusterIndexes:
                if len(c) > max_len:
                    max_i = temp_i
                    max_len = len(c)
                temp_i += 1
            self.divide(max_i)
            #self.print_img(True)
            self.saveIndex += 1
            i += 1
            self.firstIter = False

    def divide(self, cluster_index):
        self.clusterIndexes.append({})
        second_index = len(self.clusterIndexes) - 1
        means = {}
        for k in [cluster_index, second_index]:
            temp_index = random.choice(list(self.clusterIndexes[cluster_index]))
            means[k] = copy.deepcopy(dataset[temp_index])

        change = True
        while change is True:

            change = False
            mean_sums = {}
            mean_counts = {}
            for i in [cluster_index, second_index]:
                mean_sums[i] = Point(0, 0)
                mean_counts[i] = 0

            for point_i in (list(self.clusterIndexes[cluster_index]) + list(self.clusterIndexes[second_index])):
                min_distance = 1000000.0
                min_k = 0
                for k in [cluster_index, second_index]:
                    distance = dataset[point_i].get_euc_dist(means[k])
                    if distance < min_distance:
                        min_distance = distance
                        min_k = k

                if dataset[point_i].color != min_k * 10:
                    change = True

                if change:
                    if self.firstIter:
                        del self.clusterIndexes[0][point_i]
                    else:
                        del self.clusterIndexes[int(dataset[point_i].color / 10)][point_i]

                    self.clusterIndexes[min_k][point_i] = point_i

                mean_sums[min_k].x += dataset[point_i].x
                mean_sums[min_k].y += dataset[point_i].y
                mean_counts[min_k] += 1

                dataset[point_i].color = min_k * 10

            self.firstIter = False
            for k in [cluster_index, second_index]:
                if mean_counts[k] == 0:
                    mean_counts[k] = 1

                means[k].x = mean_sums[k].x / mean_counts[k]
                means[k].y = mean_sums[k].y / mean_counts[k]
                means[k].color = k * 10

        for mean in list(means.values()):
            old = 0
            for old in range(len(self.finalMeans)):
                if self.finalMeans[old].color == mean.color and not self.firstIter:
                    del self.finalMeans[old]
                    break

            self.finalMeans.append(copy.deepcopy(mean))

    def print_img(self, save):
        x_vals, y_vals = zip(*[(int(bod.x), int(bod.y)) for bod in dataset])

        plt.scatter(x_vals, y_vals, c=[point.color for point in dataset], cmap=cmap, norm=norm)

        for k in range(len(self.finalMeans)):
            plt.scatter(self.finalMeans[k].x, self.finalMeans[k].y, c="black", marker="x")

        plt.title("Divisive, k=" + str(self.k_param) + ", pocet bodov=" + str(NUM_POINTS))
        if save:
            plt.savefig("divisive" + str(self.k_param) + "_" + str(NUM_POINTS) + "_" + str(GsaveIndex) + ".jpg")
        else:
            plt.show()
        plt.clf()


def recolor_data():
    for point in dataset:
        point.color = 10000


LBOUND = -5000
RBOUND = 5000
INTERVAL = abs(RBOUND) + abs(LBOUND)
NUM_POINTS = 20000
GsaveIndex = 0
cmap, norm = from_levels_and_colors([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
                                                ['red', 'green', 'blue', "cyan", "purple", "coral", "gold", "fuchsia",
                                                 "maroon", "lime", "sienna", "brown", "indigo", "orangered", "teal",
                                                 "violet", "yellow", "yellowgreen", "orchid"])
count = 10
generate_data()
TYPE = 1

if TYPE == 1 or TYPE == 0:
    btime = time.time()
    k1 = KMeansClustering(count)
    k1.cluster()
    etime = time.time()
    print(etime - btime)
    k1.print_img(False)

if TYPE == 0:
    recolor_data()

if TYPE == 2 or TYPE == 0:
    btime = time.time()
    k2 = KMedoidClustering(count)
    k2.cluster()
    etime = time.time()
    print(etime - btime)
    k2.print_img(False)

if TYPE == 0:
    recolor_data()

if TYPE == 3 or TYPE == 0:
    btime = time.time()
    k2 = AgglomerativeClustering(count)
    k2.cluster()
    etime = time.time()
    print(etime - btime)
    k2.print_img(False)

if TYPE == 0:
    recolor_data()

if TYPE == 4 or TYPE == 0:
    btime = time.time()
    k2 = DivisiveClustering(count)
    k2.cluster()
    etime = time.time()
    print(etime - btime)
    k2.print_img(False)
