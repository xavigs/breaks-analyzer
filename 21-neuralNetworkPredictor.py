from datetime import date, datetime
import json
import pandas as pd
import numpy as np
import click

# Constants to normalize
CATEGORIES = ['WTA', 'ATP-Next', 'Davis', 'United Cup', 'ITF', 'CH', 'ATP-250', 'ATP-500', 'ATP-1000', 'ATP-Finals', 'GS', 'JJOO']
CATEGORIES_VALUE = 1 / (len(CATEGORIES) - 1)
SURFACES = ['T', 'D', 'I', 'H', 'M']
SURFACES_VALUE = 1 / (len(SURFACES) - 1)
LAST = ['22', '21', '12', '20', '02', '11', '10', '01', 'OK']
LAST_VALUE = 1 / (len(LAST) - 1)
HOME = ['NS', 'SS', 'NN', 'SN']
HOME_VALUE = 1 / (len(HOME) - 1)

@click.command()
@click.option(
    '-d', '--day',
    help = "Date to analyze break data", type = str, default = date.today().strftime("%Y-%m-%d"), show_default = True
)

def neuralNetworkPredictor(day):
    # Load parameters
    with open('parameters.json') as content:
        parameters = json.load(content)

    parameters['jump'] = [x - 1 for x in parameters['jump']]
    parameters['jump'] = [1, 2] + parameters['jump']

    # Load Excel and convert it to dataframe
    print('STEP 1: Loading Excel data...')
    breaksDF = pd.read_excel('Breaks 1r set.xlsx', sheet_name='Break', usecols='A:O', skiprows=parameters['jump'])
    breaksDF.columns.values[2] = 'SubCat.'

    # Normalize data
    print('STEP 2: Normalizing data...')
    maxValues = {
        'Quota\nVictòria\nRival': breaksDF['Quota\nVictòria\nRival'].max(),
        'Quota': breaksDF['Quota'].max()
    }
    minValues = {
        'Quota\nVictòria\nRival': breaksDF['Quota\nVictòria\nRival'].min(),
        'Quota': breaksDF['Quota'].min()
    }
    currentDate = '1900-01-01'
    currentMonth = 12
    currentYear = 2019

    for index, pick in breaksDF.iterrows():
        # Day
        if pd.isna(pick['Dia']):
            breaksDF.loc[index, 'Dia'] = currentDate
        else:
            month = int(pick['Dia'].strftime("%m"))

            if month < currentMonth:
                currentYear += 1

            currentMonth = month
            currentDate = '{}-{}'.format(currentYear, pick['Dia'].strftime("%m-%d"))
            breaksDF.loc[index, 'Dia'] = currentDate

        # Category
        if pd.isna(pick['SubCat.']) or pick['Cat.'] == 'WTA':
            category = pick['Cat.']
        else:
            category = '{}-{}'.format(pick['Cat.'], pick['SubCat.'])

        breaksDF.loc[index, 'Cat.'] = CATEGORIES.index(category.replace('ATP Cup', 'United Cup').replace('ATP-GS', 'GS')) * CATEGORIES_VALUE

        # Surface
        breaksDF.loc[index, 'Sup.'] = SURFACES.index(pick['Sup.']) * SURFACES_VALUE

        # Last games
        breaksDF.loc[index, 'Últim'] = LAST.index(str(pick['Últim'])) * LAST_VALUE

        # Opponent odd
        column = 'Quota\nVictòria\nRival'
        breaksDF.loc[index, column] = (pick[column] - minValues[column]) / (maxValues[column] - minValues[column])

        # Home
        home = '{}{}'.format(pick['Local'], pick['Rival\nLocal'])
        breaksDF.loc[index, 'Local'] = HOME.index(home) * HOME_VALUE

        # Odd
        column = 'Quota'
        breaksDF.loc[index, column] = (pick[column] - minValues[column]) / (maxValues[column] - minValues[column])

        # Probabilitat
        column = 'Prob.\nNostra'
        probability = pick[column]

        if probability <= 0.75:
            breaksDF.loc[index, column] = 0
        elif probability <= 0.8:
            breaksDF.loc[index, column] = 0.2
        elif probability <= 0.85:
            breaksDF.loc[index, column] = 0.4
        elif probability <= 0.90:
            breaksDF.loc[index, column] = 0.6
        elif probability <= 0.95:
            breaksDF.loc[index, column] = 0.8
        else:
            breaksDF.loc[index, column] = 1

        # Result
        if pick['Res.'] == "W":
            breaksDF.loc[index, 'Res.'] = 1
        elif pick['Res.'] == "N":
            breaksDF.loc[index, 'Res.'] = 0.5
        elif pick['Res.'] == "L":
            breaksDF.loc[index, 'Res.'] = 0

    breaksDF = breaksDF.drop(['SubCat.', 'Rival\nLocal', 'Val.'], axis=1)
    breaksDF.columns = ['Day', 'Category', 'Surface', 'Player', 'Opponent', 'Last Games', 'Opponent Odd', 'Home', 'Odd', 'Probability', 'Bookie Probability', 'Result']

    # Neural network sigmoid (0-1) functions
    def sigmoid(x):
        return 1.0/(1.0 + np.exp(-x))

    def sigmoid_derivada(x):
        return sigmoid(x)*(1.0-sigmoid(x))

    # Neural network class
    class NeuralNetwork:

        def __init__(self, layers):
            self.activation = sigmoid
            self.activation_prime = sigmoid_derivada

            # Init weights
            self.weights = []
            self.deltas = []

            # Set random values
            '''for i in range(1, len(layers) - 1):
                r = 2 * np.random.random((layers[i-1] + 1, layers[i] + 1)) -1
                self.weights.append(r)

            r = 2 * np.random.random((layers[i] + 1, layers[i+1])) - 1
            self.weights.append(r)'''

        def fit(self, X, y, learning_rate=0.2, epochs=100000):
            origin = X
            ones = np.atleast_2d(np.ones(X.shape[0]))
            X = np.concatenate((ones.T, X), axis=1)

            for k in range(epochs):
                i = np.random.randint(X.shape[0])
                a = [X[i]]

                for l in range(len(self.weights)):
                    dot_value = np.dot(a[l], self.weights[l])
                    activation = self.activation(dot_value)
                    a.append(activation)

                error = y[i] - a[-1]
                deltas = [error * self.activation_prime(a[-1])]

                for l in range(len(a) - 2, 0, -1):
                    deltas.append(deltas[-1].dot(self.weights[l].T)*self.activation_prime(a[l]))

                self.deltas.append(deltas)
                deltas.reverse()

                # Backpropagation
                for i in range(len(self.weights)):
                    layer = np.atleast_2d(a[i])
                    delta = np.atleast_2d(deltas[i])
                    self.weights[i] += learning_rate * layer.T.dot(delta)

                if k % 10000 == 0: print('epochs:', k)

        def predict(self, x):
            ones = np.atleast_2d(np.ones(x.shape[0]))
            a = np.concatenate((np.ones(1).T, np.array(x)), axis=0)
            for l in range(0, len(self.weights)):
                a = self.activation(np.dot(a, self.weights[l]))
            return a

        def print_weights(self):
            print("CONNECTION WEIGHTS")
            for i in range(len(self.weights)):
                print(self.weights[i])

        def get_deltas(self):
            return self.deltas

    # NEURAL NETWORK !!
    nn = NeuralNetwork([7, 4, 2, 1])
    picksToPredict = breaksDF.loc[breaksDF['Day'] == '2024-10-31']
    dfIndex = picksToPredict.index[0]
    picksToPredict = picksToPredict.values.tolist()
    Z = np.array(picksToPredict)

    picksForTrain = breaksDF.iloc[0:100][['Category', 'Surface', 'Last Games', 'Opponent Odd', 'Home', 'Odd', 'Probability']].values.tolist()
    resultsForTrain = breaksDF.iloc[0:100][['Result']].values.tolist()

    X = np.array(picksForTrain)
    y = np.array(resultsForTrain)
    nn.fit(X, y, learning_rate=0.01, epochs=100000)

    nn.weights = [
        [
            [-0.75236525, -0.62916982, 0.96004899, -0.51154925, -0.74485989],
            [-0.25362612, 0.74649676, 0.85557482, -0.84761539, -0.86765543],
            [-0.57280527, -0.39347571, -0.96193493, 0.30362607, -1.0480467],
            [0.75325056, 0.38256371, -0.89355923, 0.82825342, 0.01985758],
            [-0.62154981, 0.88283088, 0.92455119, -0.08448481, -0.40125866],
            [-0.10525981, -0.4280205, -0.38946615, 0.37378263, 0.6036072],
            [-1.41029252, 0.46751052, -0.69194862, 0.59329885, -0.20950866],
            [0.33792327, -0.60927939, 0.69181502, 0.59599815, -0.08188759]
        ],
        [
            [-1.06347354, -1.02706003, 1.02017579],
            [0.03484287, -0.07531554, -0.73389368],
            [-1.00591573, -0.29968427, -0.21462693],
            [0.71624517, 0.41621088, 0.18934073],
            [0.08098775, -0.22955955, 0.64915552]
        ],
        [
            [-0.56095208],
            [-0.54879729],
            [1.13028711]
        ]
    ]

    for e in Z:
        prediction = nn.predict(e)
        day = breaksDF.iloc[dfIndex]['Day'].strftime("%Y-%m-%d")
        probability = round(prediction[0] * 100, 2)
        bookie = round(breaksDF.iloc[dfIndex]['Bookie Probability'] * 100, 2)
        value = probability / bookie

        if probability > bookie and value >= 1.25:
            odd = round(1 / breaksDF.iloc[dfIndex]['Bookie Probability'], 2)
            print(day)
            print('{} vs. {}'.format(breaksDF.iloc[dfIndex]['Player'], breaksDF.iloc[dfIndex]['Opponent']))
            print('Odd: {}'.format(odd))
            print('Probability: {}%'.format(probability))
            print('Bookie Probability: {}'.format(bookie))
            print('Value: {}'.format(value))

        dfIndex += 1

if __name__ == '__main__':
    neuralNetworkPredictor()