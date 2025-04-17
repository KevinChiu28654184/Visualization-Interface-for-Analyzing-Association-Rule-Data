import pandas as pd
import numpy as np
import itertools
import os
import math

# data loader
class Loader():
    def __init__(self) -> None:
        self.__data_exist = False
        self.__data_df = None
        self.__data_np = None
        self.__path = None
    
    def open_file(self, path):
        if self.__data_exist:
            self.reset()
            print("loader reset")
        self.__path = path  
        if os.path.isfile(self.__path):
            self.__data_exist = True
            self.__data_df = pd.read_csv(path).loc[:,["antecedents","consequents", "oddsratio"]]
            self.__data_df.sort_values(["oddsratio"], ascending=False,inplace=True)
            self.__data_np = self.__data_df.to_numpy()
            print("open success")
        else:
            print("invalid url")
    
    def get_data(self, type_="np"):
        if not self.__data_exist:
            print("no data")
            return None
        if type_ == "np":
            return self.__data_np
        elif type_ == "df":
            return self.__data_df
    
    def get_path(self):
        return self.__path
    
    def reset(self):
        self.__data_exist = False
        self.__data_df = None
        self.__data_np = None
        self.__path = None

# data filter
class Filter():

    ant_col = 0
    con_col = 1
    odd_col = 2
    
    def __init__(self) -> None:
        pass

    def get_unique_tags(self, data):
        unique = []
        for i in range(data.shape[0]):
            unique = np.append(unique, data[i].split(", "))
        unique = np.unique(unique)
        return unique

    def filter(self, data, col, threshold):
        if col == "oddsratio":
            return self.__by_oddsratio(data, threshold)
        elif col == "antecedents":
            return self.__by_antecedents(data, threshold)
        elif col == "consequents":
            return self.__by_consequents(data, threshold)
        
        
        else:
            print("invalid col")
            return None

    def __by_oddsratio(self, data, threshold):
        temp = []
        for i in range(data.shape[0]):
            if data[i, self.odd_col] >= threshold:
                temp.append(i)
        return np.array([data[i] for i in temp])
        

    def __by_antecedents(self, data, threshold):
        temp = []
        for i in range(data.shape[0]):
            if data[i, self.ant_col].count(threshold) == 1:
                temp.append(i)
        return np.array([data[i] for i in temp])

    def __by_consequents(self, data, threshold):
        temp = []
        for i in range(data.shape[0]):
            if data[i, self.con_col].count(threshold) == 1:
                temp.append(i)
        return np.array([data[i] for i in temp])
        


# position process
class Locator():
    def __init__(self) -> None:
        pass

    def get_pos(self, ant, con, odd, pos_type="random"):
        if pos_type == "random":
            return self.__random(ant, con, odd)
        elif pos_type == "rand_adj":
            return self.__rand_adj(ant, con , odd)
        elif pos_type == "chip":
            return self.__chip(ant, con , odd)
        elif pos_type == "chip_adj":
            return self.__chip_adj(ant, con, odd)
        elif pos_type == "pre_pos":
            return self.__pre_pos(ant, con, odd)
        elif pos_type == "pre_adj":
            return self.__pre_adj(ant, con, odd)
        else:
            print("pos type error")
            return None

    def __random(self, ant, con, odd):
        pos = {}

        point = np.append(ant, con)
        point = np.unique(point)
        
        random_list = list(itertools.product(range(1, 150), range(1, 150)))
        potential_pos = np.random.permutation(random_list)[:point.shape[0]]

        for i in range(point.shape[0]):
            pos[point[i]] = potential_pos[i]

        return pos

    def __rand_adj(self, ant, con, odd):
        pos = self.__random(ant,con,odd)

        point = np.unique(np.append(ant,con))

        wei = {}
        for i in range(point.shape[0]):
            wei[point[i]] = 0
        for i in range(ant.shape[0]):
            wei[ant[i]] += odd[i]
            wei[con[i]] += odd[i]

        epochs = 3
        for _ in range(epochs):
            for i in range(ant.shape[0]):
                if odd[i] == 1:
                    break
                ant_pos = pos[ant[i]]
                con_pos = pos[con[i]]

                mid_pos = (ant_pos * wei[ant[i]] + con_pos * wei[con[i]]) / (wei[ant[i]] + wei[con[i]])
                    
                ant_pos = (ant_pos - mid_pos) / (2 * odd[i]) + mid_pos
                con_pos = (con_pos - mid_pos) / (2 * odd[i]) + mid_pos

                pos[ant[i]] = ant_pos
                pos[con[i]] = con_pos

        return pos

    def __chip(self, ant, con, odd):
        pos = {}

        point = np.unique(np.append(ant,con))
        chip = self.__get_unique_chip(point)
        
        random_list = list(itertools.product(range(1, 150), range(1, 150)))
        potential_pos = np.random.permutation(random_list)[:chip.shape[0]]

        for i in range(chip.shape[0]):
            pos[chip[i]] = potential_pos[i]

        for i in range(point.shape[0]):
            temp = point[i].split(", ")
            if point[i] in pos:
                continue
            pos[point[i]] = np.zeros(2)
            for c in temp:
                pos[point[i]] = pos[point[i]] + pos[c]
            pos[point[i]] = pos[point[i]] / len(temp)

        return pos
    
    def __chip_adj(self, ant, con, odd):
        pos = self.__chip(ant, con, odd)

        point = np.unique(np.append(ant,con))

        wei = {}
        for i in range(point.shape[0]):
            wei[point[i]] = 0
        for i in range(ant.shape[0]):
            wei[ant[i]] += odd[i]
            wei[con[i]] += odd[i]

        epochs = 3
        for _ in range(epochs):
            for i in range(ant.shape[0]):
                if odd[i] == 1:
                    break
                ant_pos = pos[ant[i]]
                con_pos = pos[con[i]]

                mid_pos = (ant_pos * wei[ant[i]] + con_pos * wei[con[i]]) / (wei[ant[i]] + wei[con[i]])
                    
                ant_pos = (ant_pos - mid_pos) / (2 * odd[i]) + mid_pos
                con_pos = (con_pos - mid_pos) / (2 * odd[i]) + mid_pos

                pos[ant[i]] = ant_pos
                pos[con[i]] = con_pos

        return pos

    def __pre_pos(self, ant, con, odd):
        pos = {}
        K = odd[0]

        random_list = list(itertools.product(range(1, 150), range(1, 150)))
        potential_pos = np.random.permutation(random_list)
        counter = 0

        for i in range(ant.shape[0]):
            if (ant[i] in pos) and (con[i] in pos):
                continue
            if (not ant[i] in pos) and (not con[i] in pos):
                pos[ant[i]] = potential_pos[counter]
                counter += 1

                ang = np.random.uniform(-math.pi/2, math.pi/2)
                L = K / odd[i]
                pos[con[i]] = pos[ant[i]] + np.array([L * math.cos(ang), L * math.sin(ang)])
            
            elif not con[i] in pos:
                ang = np.random.uniform(-math.pi/2, math.pi/2)
                L = K / odd[i]
                pos[con[i]] = pos[ant[i]] + np.array([L * math.cos(ang), L * math.sin(ang)])

            elif not ant[i] in pos:
                ang = np.random.uniform(math.pi / 2, 3 * math.pi / 2)
                L = K / odd[i]
                pos[ant[i]] = pos[con[i]] + np.array([L * math.cos(ang), L * math.sin(ang)])
            
            else:
                print("pos error")
                break

        return pos

    def __pre_adj(self, ant, con, odd):
        pos = self.__pre_pos(ant, con, odd)
        alpha = 0.9
        K = odd[0]
        point = np.unique(np.append(ant, con))

        wei = {}
        for i in range(point.shape[0]):
            wei[point[i]] = 0
        for i in range(ant.shape[0]):
            wei[ant[i]] += odd[i]
            wei[con[i]] += odd[i]

        epochs = 50
        for _ in range(epochs):
            for i in range(ant.shape[0]):
                D = np.linalg.norm(pos[ant[i]] - pos[con[i]])
                L = K / odd[i]
                mid_pos = (pos[ant[i]] * wei[ant[i]] + pos[con[i]] * wei[con[i]]) / (wei[ant[i]] + wei[con[i]])
                ant_pos = pos[ant[i]]
                con_pos = pos[con[i]]

                if abs(L - D) < 0.01:
                    continue
                if L > D:
                    ant_pos = (ant_pos - mid_pos) / alpha + mid_pos
                    con_pos = (con_pos - mid_pos) / alpha + mid_pos
                    
                elif L < D:
                    ant_pos = (ant_pos - mid_pos) * alpha + mid_pos
                    con_pos = (con_pos - mid_pos) * alpha + mid_pos
                else:
                    print("error")

                pos[ant[i]] = ant_pos
                pos[con[i]] = con_pos

        return pos

    def __get_unique_chip(self, data):
        unique = []
        for i in range(data.shape[0]):
            unique = np.append(unique, data[i].split(", "))
        unique = np.unique(unique)
        return unique
