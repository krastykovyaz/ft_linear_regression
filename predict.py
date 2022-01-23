import pickle

class Predictor:
    def __init__(self):
        try:
            self.mileage = float(input("Mileage:"))
        except Exception as er:
            print(er)
            print('Enter mileage in km as number !')
            self.__init__()
        try:
            with open('data.pickle', 'rb') as f:
                coefficients = pickle.load(f)
            self.theta0 = coefficients['theta0']
            self.theta1 = coefficients['theta1']
        except Exception as er:
            print(er)
            print('File with thetas is worng !')
            self.__init__()

    def get_price(self):
        return round(self.theta0 + self.theta1 * self.mileage, 2)

        

if __name__ == '__main__':
    predictor = Predictor()
    print(predictor.get_price())
