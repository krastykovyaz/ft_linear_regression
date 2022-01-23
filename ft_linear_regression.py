import os
import pandas as pd
import numpy as np #Data manipulation
import matplotlib.pyplot as plt # Visualization
import seaborn as sns #Visualization
import pickle # save data
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

class Reader:

    @staticmethod
    def read_files():
        files = [file for file in os.listdir() \
            if file.endswith('.xlsx') or\
                file.endswith('.csv')]
        for i, f in enumerate(files):
            print(i, '-', f)
        print('Chooce the number of the file:')
        return files

    @staticmethod
    def read_file(files):
        idx = input()
        idx = int(idx)
        try:
            df = pd.read_excel(files[idx])
        except:
            df = pd.read_csv(files[idx])
        if 'km' not in df.columns or 'price' not in df.columns:
            return "Check the name of the columns. They are should be name 'km' and 'price'!"
        return df

class DataMaster:
    def __init__(self, df):
        self.df = df
        self.mileage = list(df['km'])
        self.price = list(df['price'])
        self.norm_mileage = normalaze_data(self.mileage)
        self.norm_price = normalaze_data(self.price)

    @staticmethod
    def get_theta(mileage, price, theta0, theta1, flag): 
        res = 0
        for i in range(len(mileage)):
            value = theta0 + theta1 * mileage[i]
            if flag == '1':
                res += (value - price[i]) * mileage[i]
            else:
                res += value - price[i]
        return res / len(mileage)

    def gradient_descent(self):
        theta0 = 0 
        theta1 = 0
        learning_rate = 0.1
        i = 1
        while i < 10000: 
            tmp_theta0 = learning_rate * self.get_theta(self.norm_mileage, self.norm_price, theta0, theta1, '0')
            tmp_theta1 = learning_rate * self.get_theta(self.norm_mileage, self.norm_price, theta0, theta1, '1')
            theta0 -= tmp_theta0
            theta1 -= tmp_theta1
            if abs(tmp_theta0 < 0.000001) and abs(tmp_theta1) < 0.000001:
                break
            i += 1
        print('Number of iterations', i)
        return theta0, theta1
    
    def plot_data(self, theta0, theta1):
         
        theta0 = theta0 * max(self.price)
        theta1 = theta1 * (max(self.price) / max(self.mileage))
        with open('data.pickle', 'wb') as f:
            pickle.dump({'theta0':theta0,"theta1":theta1}, f)
        print('\n\n')
        print('Theta0 :', theta0)
        print('Theta1 :', theta1)
        results = []
        for i in range(len(self.mileage)):
            results.append(theta0 + self.mileage[i] * theta1)
        sns.scatterplot(self.mileage, self.price)
        sns.scatterplot(self.mileage, results)
        plt.ylabel("Price, $")
        plt.xlabel("Mileage, km")
        plt.show()


def normalaze_data(data):
        normal = []
        for i in data:
            normal.append(i / max(data))
        return normal    

    

if __name__=='__main__':
    reader = Reader()
    file = reader.read_files()
    df = reader.read_file(file)
    if type(df) == 'str':
        print(df)
        exit(1)
    data_master = DataMaster(df)
    theta0, theta1 = data_master.gradient_descent()
    data_master.plot_data(theta0, theta1)

    

