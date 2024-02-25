# -*- coding: utf-8 -*-
import sys
import openpyxl
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import *
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
systemsObj = objects.Systems(breaksDB)

def printArray(data):
    print("[")

    for element in data:
        print("\t{")

        for key in element:
            print("\t\t'" + str(key) + "': " + str(element[key]))

        print("\t}")

    print("]")

with open("parameters.json") as content:
    parameters = json.load(content)

# Variables
SYSTEMS_TO_SHOW = (
    "Sistema 3",
    "Sistema NAS",
    "Sistema D1SITIS",
    "Sistema Experimental",
    "Sistema Experimental I",
    "Sistema Experimental II",
    "Sistema Experimental IV",
    "Sistema Experimental V",
    "Sistema Experimental VI",
    "Sistema Experimental VII",
    "Sistema Experimental IX",
    "Sistema Experimental X",
    "Sistema Experimental XI",
    "Sistema Experimental XII",
    "Sistema Experimental XIII",
    "Sistema Experimental XIV"
)
systems = {}
formula = {}
formula['units'] = 0
formula['num-picks'] = 0
formula['stake'] = 0.0
formula['periods'] = {}
formula['games'] = []

for system in parameters['systems']:
    systems[system['name']] = {}
    systems[system['name']]['games'] = []
    systems[system['name']]['25'] = 0.0
    systems[system['name']]['50'] = 0.0
    systems[system['name']]['75'] = 0.0
    systems[system['name']]['100'] = 0.0
    systems[system['name']]['150'] = 0.0
    systems[system['name']]['200'] = 0.0
    systems[system['name']]['250'] = 0.0
    systems[system['name']]['300'] = 0.0
    systems[system['name']]['350'] = 0.0
    systems[system['name']]['400'] = 0.0
    systems[system['name']]['450'] = 0.0
    systems[system['name']]['500'] = 0.0
    systems[system['name']]['550'] = 0.0
    systems[system['name']]['600'] = 0.0
    systems[system['name']]['units'] = 0.0
    systems[system['name']]['num-picks'] = 0
    systems[system['name']]['total-months'] = 0
    systems[system['name']]['positive-months'] = 0
    systems[system['name']]['10plus-months'] = 0
    systems[system['name']]['periods'] = {}

    if "future" in system:
        systems[system['name']]['start'] = system['start-text']
        systems[system['name']]['start-bank'] = system['start-bank']
        systems[system['name']]['future'] = {}
        systems[system['name']]['future']['units'] = 0
        systems[system['name']]['future']['num-picks'] = 0
        systems[system['name']]['future']['yield'] = 0.0

    for period in parameters['periods']:
        if period['type'] == 1:
            systems[system['name']]['total-months'] += 1
            formula['periods'][period['keyword']] = {}
            formula['periods'][period['keyword']]['name'] = period['name']
            formula['periods'][period['keyword']]['units'] = 0.0
            formula['periods'][period['keyword']]['num-picks'] = 0
            formula['periods'][period['keyword']]['stake'] = 0.0

        systems[system['name']]['periods'][period['keyword']] = {}
        systems[system['name']]['periods'][period['keyword']]['name'] = period['name']
        systems[system['name']]['periods'][period['keyword']]['type'] = period['type']
        systems[system['name']]['periods'][period['keyword']]['units'] = 0.0
        systems[system['name']]['periods'][period['keyword']]['num-picks'] = 0

# Open Workbook
workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", read_only = True, data_only = True)

# Get Sheet Object by names
sheet = workbook['Break']

for row in sheet.iter_rows(min_row = 4, max_row = parameters['last-row']):
    rowNumber = row[0].row
    print("Reading the row nº {}...".format(rowNumber))

    if row[0].value is not None:
        date = row[0].value

    if not rowNumber in parameters['jump']:
        valid = True

        for criteria in parameters['dismiss']:
            column = ord(criteria['col']) - 65

            if criteria['operator'] == "=":
                if row[column].value == criteria['value']:
                    valid = False
                    break
                elif criteria['operator'] == "<":
                    if row[column].value < criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == ">":
                    if row[column].value > criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == ">=":
                    if row[column].value >= criteria['value']:
                        valid = False
                        break
                elif criteria['operator'] == "<>":
                    if row[column].value != criteria['value']:
                        valid = False
                        break

        if valid:
            found = False

            for system in parameters['systems']:
                validForSystem = False

                for conditionGroup in system['conditions']:
                    numConditions = len(conditionGroup)
                    satisfiedConditions = 0

                    for condition in conditionGroup:
                        column = ord(condition['col']) - 65

                        if condition['operator'] == "=":
                            if row[column].value == condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == "<":
                            if row[column].value < condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == ">":
                            if row[column].value > condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == ">=":
                            if row[column].value >= condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == "<>":
                            if row[column].value != condition['value']:
                                satisfiedConditions += 1

                    if numConditions == satisfiedConditions:
                        validForSystem = True
                        break

                if validForSystem:
                    game = {}
                    game['date'] = date
                    game['player'] = row[4].value
                    game['opponent'] = row[5].value
                    game['odd'] = row[10].value
                    game['result'] = row[14].value

                    # Balance
                    if row[14].value == "L":
                        balance = -1
                    elif row[14].value == "N":
                        balance = 0
                    else:
                        balance = game['odd'] - 1

                    #systems[system['name']]['games'].append(game)
                    systems[system['name']]['units'] += balance
                    systems[system['name']]['num-picks'] += 1
                    systems[system['name']]['yield'] = round(systems[system['name']]['units'] * 100 / systems[system['name']]['num-picks'], 2)

                    if systems[system['name']]['num-picks'] == 25:
                        systems[system['name']]['25'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 50:
                        systems[system['name']]['50'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 75:
                        systems[system['name']]['75'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 100:
                        systems[system['name']]['100'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 150:
                        systems[system['name']]['150'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 200:
                        systems[system['name']]['200'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 250:
                        systems[system['name']]['250'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 300:
                        systems[system['name']]['300'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 350:
                        systems[system['name']]['350'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 400:
                        systems[system['name']]['400'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 450:
                        systems[system['name']]['450'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 500:
                        systems[system['name']]['500'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 550:
                        systems[system['name']]['550'] = systems[system['name']]['yield']
                    elif systems[system['name']]['num-picks'] == 600:
                        systems[system['name']]['600'] = systems[system['name']]['yield']

                    if "future" in system and rowNumber >= system['future']:
                        systems[system['name']]['future']['units'] += balance
                        systems[system['name']]['future']['num-picks'] += 1
                        systems[system['name']]['future']['yield'] = round(systems[system['name']]['future']['units'] * 100 / systems[system['name']]['future']['num-picks'], 2)

                    for formulaSystem in parameters['formula']:
                        if not found and system['name'] == formulaSystem['system']:
                            found = True
                            game['stake'] = formulaSystem['stake']
                            formula['games'].append(game)
                            formula['num-picks'] += 1
                            formula['units'] += balance
                            formula['stake'] += formulaSystem['stake']
                            formula['yield'] = round(formula['units'] * 100 / formula['stake'], 2)

                            for period in parameters['periods']:
                                if rowNumber >= period['first-row'] and rowNumber <= period['last-row'] and period['type'] == 1:
                                    formula['periods'][period['keyword']]['units'] += balance * formulaSystem['stake']
                                    formula['periods'][period['keyword']]['num-picks'] += 1
                                    formula['periods'][period['keyword']]['stake'] += formulaSystem['stake']
                                    formula['periods'][period['keyword']]['yield'] = round(formula['periods'][period['keyword']]['units'] * 100 / formula['periods'][period['keyword']]['stake'], 2)

                    for period in parameters['periods']:
                        if rowNumber >= period['first-row'] and rowNumber <= period['last-row']:
                            systems[system['name']]['periods'][period['keyword']]['units'] += balance
                            systems[system['name']]['periods'][period['keyword']]['num-picks'] += 1
                            systems[system['name']]['periods'][period['keyword']]['yield'] = round(systems[system['name']]['periods'][period['keyword']]['units'] * 100 / systems[system['name']]['periods'][period['keyword']]['num-picks'], 2)

'''
    PLOTLY!!!!!
'''
sistemes = ['Sistema 1'] * 20
factors = ['Yield:<br>21,0%', 'Monthly picks:<br>18,5', 'Positive months:<br>8', 'Plus 10% months:<br>5', 'Empty']

# Dades de gràfics donut per cada sistema
donut_data = [[15, 35, 25, 20, 5], [20, 30, 25, 25, 0], [10, 40, 30, 20, 0], [30, 20, 15, 35, 0],
              [25, 25, 30, 20, 0], [18, 22, 30, 30, 0], [12, 28, 30, 30, 0], [22, 28, 20, 30, 0],
              [35, 15, 25, 25, 0], [20, 30, 25, 25, 0], [10, 40, 30, 20, 0], [30, 20, 15, 35, 0],
              [25, 25, 30, 20, 0], [18, 22, 30, 30, 0], [12, 28, 30, 30, 0], [22, 28, 20, 30, 0],
              [35, 15, 25, 25, 0], [20, 30, 25, 25, 0], [10, 40, 30, 20, 0], [30, 20, 15, 35, 0]]

# Creació de la graella de subgràfics
'''specs = [[{'type': 'domain'}] * 5 for _ in range(4)]
specs[0][0] = {'type': 'scatter'}  # Assignar el tipus 'scatter' a la primera cel·la
print(specs)
exit()'''
#specs = [[{'type': 'scatter'}, {'type': 'pie'}] for _ in range(4)]
#specs = [[{"type": "pie"}] * 20, [{"type": "scatter"}]]
#specs=[[{"type": "xy"}, {"type": "polar"}], [{"type": "domain"}, {"type": "scene"}]],
#specs=[[{"type": "xy"}, {"type": "pie"}]]
specs = [[{'type': 'pie'}] * 5 for _ in range(4)]
fig = make_subplots(rows=4, cols=5, subplot_titles=SYSTEMS_TO_SHOW, specs=specs)
#fig = make_subplots(rows=4, cols=5, subplot_titles=sistemes)

# Afegir gràfics donut i gestionar clics
for i in range(4):
    for j in range(5):
        idx = i * 5 + j
        donut_fig = go.Figure(go.Pie(labels=factors, values=donut_data[idx], hole=0.6, hoverinfo="percent", textinfo="label", marker_colors=["#001440", "#fd5300", "#104fb1", "#fdc505", "#ffffff"]))
        donut_fig.update_layout(title_text=sistemes[idx], showlegend=False, annotations=[dict(text=f"<b>{f}</b>", x=0.5, y=-0.1, font=dict(size=10), showarrow=False) for f in factors])
        #fig.add_trace(go.Scatter(), row=i + 1, col=j + 1)
        fig.add_trace(donut_fig['data'][0], row=i + 1, col=j + 1)
        button = dict(label=f'Detall {sistemes[idx]}', method='update', args=[{'visible': [False] * len(sistemes) * 2}, {'visible': [idx * 2 + 1, idx * 2]}])
        #fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[button])])

# Configurar esdeveniments de clic
'''for i, sistema in enumerate(sistemes):
    button = dict(label=f'Detall {sistema}', method='update', args=[{'visible': [False] * len(sistemes)}, {'visible': [idx == i for idx in range(len(sistemes))]}])
    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[button])])'''

# Afegir gràfics de barres amb línia superposada pel detall
'''detall_fig = go.Figure()

# Dades de gràfic de barres i línia per detall del sistema
bar_data = [20, 30, 25, 25]
line_data = [15, 25, 20, 35]

detall_fig.add_trace(go.Bar(x=factors, y=bar_data, name='Barres'))
detall_fig.add_trace(go.Scatter(x=factors, y=line_data, mode='lines', name='Línia'))'''

# Actualitzar títols i mostrar gràfics
fig.update_layout(title={'text': '<b>System analysis</b>', 'font': {'size': 24}}, title_x=0.5, showlegend=False)
#detall_fig.update_layout(title_text='System detail', showlegend=True)

#fig.show()
#detall_fig.show()

'''
    END PLOTLY!!!
'''

# Show charts
plotPySystems = []

for systemName, systemData in sorted(systems.items()):
    if 'Sistema' in systemName:
        origSystemName = systemName
        systemName = systemName.split("-")[1]
        plotPySystems.append(systemName)

specs = [[{'type': 'pie'}] * 5 for _ in range(5)]
fig = make_subplots(rows=5, cols=5, subplot_titles=plotPySystems, specs=specs)
i = 0
j = 0

for systemName, systemData in sorted(systems.items()):
    if 'Sistema' in systemName:
        monthlyPicks = round(systemData['num-picks'] / systemData['total-months'], 2)
        positiveMonths = 0
        plusMonths = 0

        for period in systemData['periods']:
            if systemData['periods'][period]['type'] == 1 and systemData['periods'][period]['units'] > 0:
                positiveMonths += 1

                if systemData['periods'][period]['yield'] >= 10:
                    plusMonths += 1

        factors = ['Yield:<br>{}%'.format(systemData['yield']), 'Monthly picks:<br>{}'.format(monthlyPicks), 'Positive months:<br>{}'.format(positiveMonths), 'Plus 10% months:<br>{}'.format(plusMonths), 'Empty']
        yieldPct = float(systemData['yield'])
        positiveMonthsEval = round(positiveMonths * 25.0 / systemData['total-months'], 2)
        plusMonthsEval = round(plusMonths * 25.0 / systemData['total-months'], 2)

        if yieldPct < 20.0:
            yieldEval = round(yieldPct * 25.0 / 20.0, 2)
        else:
            yieldEval = 25.0

        if monthlyPicks < 20.0:
            monthlyPicksEval = round(monthlyPicks * 25.0 / 20.0, 2)
        else:
            monthlyPicksEval = 25.0

        empty = 100.0 - yieldEval - monthlyPicksEval - positiveMonthsEval - plusMonthsEval

        donut_data = [yieldEval, monthlyPicksEval, positiveMonthsEval, plusMonthsEval, empty]
        donut_fig = go.Figure(go.Pie(labels=factors, values=donut_data, hole=0.6, hoverinfo="percent", textinfo="label", marker_colors=["#001440", "#fd5300", "#104fb1", "#fdc505", "#ffffff"]))
        donut_fig.update_layout(title_text=systemName, showlegend=False, annotations=[dict(text=f"<b>{f}</b>", x=0.5, y=-0.1, font=dict(size=10), showarrow=False) for f in factors])
        fig.add_trace(donut_fig['data'][0], row=i + 1, col=j + 1)
        j += 1

        if j == 5:
            j = 0
            i += 1

fig.update_layout(title={'text': '<b>System analysis</b>', 'font': {'size': 24}}, title_x=0.5, showlegend=False)
fig.show()
exit()
# Show text in terminal
for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        origSystemName = systemName
        systemName = systemName.split("-")[1]
        print("\n~~ " + systemName + " ~~\n")
        print("\t* Unitats: " + str(round(systemData['units'],2)) + " uts.")
        print("\t* Nº picks: " + str(systemData['num-picks']))
        print("\t* Yield: " + str(systemData['yield']) + " %")
        positiveMonths = 0
        plusMonths = 0

        for period in systemData['periods']:
            if systemData['periods'][period]['type'] == 1 and systemData['periods'][period]['units'] > 0:
                positiveMonths += 1

                if systemData['periods'][period]['yield'] >= 10:
                    plusMonths += 1

        print("\t* Mesos totals: {}".format(systemData['total-months']))
        print("\t* Mesos positius: " + str(positiveMonths))
        print("\t* Mesos amb més del 10% de yield: " + str(plusMonths))
        print("\t* Picks mensuals: " + str(round(systemData['num-picks'] / systemData['total-months'], 2)))
        print("\t* Detall per mesos:\n")
        bank = 100.00
        stake = 2.50

        for periodKeyword, periodData in sorted(systemData['periods'].items()):
            if periodData['type'] == 1:
                try:
                    profit = round(periodData['units'] * stake, 2)
                    new_bank = bank + profit
                    print("\t\t-> " + periodData['name'] + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: " + str(periodData['yield']) + " %\t\tBank final: " + str(new_bank) + u" \u20ac")
                    bank = new_bank

                    if periodData['name'] == systemData['start-bank']:
                        systems[origSystemName]['initial-bank'] = bank

                    stake = round(bank / 40, 2)
                except Exception as e:
                    print("\t\t-> " + periodData['name'] + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: 0.00 %")

        systems[origSystemName]['end-bank'] = bank

        if "future" in systemData:
            print("\n\t* Dades futures:\n")
            print("\t\t-> Unitats: " + str(round(systemData['future']['units'],2)) + " uts.")
            print("\t\t-> Nº picks: " + str(systemData['future']['num-picks']))
            print("\t\t-> Yield: " + str(systemData['future']['yield']) + " %")

# INSERT INTO DATABASE
systemsObj.empty()
for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemDB = {}
        systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").split("-")[1]
        if systemName.isnumeric():
            systemName = "Sist. {}".format(systemName)

        systemDB['name'] = systemName
        systemDB['start'] = systemData['start']
        systemDB['num-picks'] = systemData['future']['num-picks']
        systemDB['yield'] = systemData['future']['yield']
        systemDB['start-bank'] = systemData['initial-bank']
        systemDB['end-bank'] = systemData['end-bank']
        systemDB['global'] = systemData['yield']
        systemsObj.create(systemDB)

print("\n~~ Intervals ~~\n")
sys.stdout.write("------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n| Nº picks |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + systemName + " |")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    25    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['25']) + " %")
            leftChars = len(systemName) - len(str(systemData['25']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    50    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['50']) + " %")
            leftChars = len(systemName) - len(str(systemData['50']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    75    |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['75']) + " %")
            leftChars = len(systemName) - len(str(systemData['75']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    100   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['100']) + " %")
            leftChars = len(systemName) - len(str(systemData['100']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    150   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['150']) + " %")
            leftChars = len(systemName) - len(str(systemData['150']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    200   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['200']) + " %")
            leftChars = len(systemName) - len(str(systemData['200']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    250   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['250']) + " %")
            leftChars = len(systemName) - len(str(systemData['250']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    300   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['300']) + " %")
            leftChars = len(systemName) - len(str(systemData['300']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    350   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['350']) + " %")
            leftChars = len(systemName) - len(str(systemData['350']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    400   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['400']) + " %")
            leftChars = len(systemName) - len(str(systemData['400']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    450   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['450']) + " %")
            leftChars = len(systemName) - len(str(systemData['450']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    500   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['500']) + " %")
            leftChars = len(systemName) - len(str(systemData['500']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    550   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['550']) + " %")
            leftChars = len(systemName) - len(str(systemData['550']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")

sys.stdout.write("\n|    600   |")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write(" " + str(systemData['600']) + " %")
            leftChars = len(systemName) - len(str(systemData['600']))

            for i in range(1, leftChars):
                sys.stdout.write(" ")

            sys.stdout.write("|")

sys.stdout.write("\n------------")

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        if systemName in SYSTEMS_TO_SHOW and "future" in systemData:
            systemName = systemName.replace("Sistema ", "").replace("Experimental", "Exp.").center(7)
            sys.stdout.write("-")

            for char in systemName:
                sys.stdout.write("-")

            sys.stdout.write("--")
sys.stdout.write("\n")
exit()
print("\n\n~~ Fórmula Actual ~~\n")
print("\t* Unitats: " + str(round(formula['units'],2)) + " uts.")
print("\t* Nº picks: " + str(formula['num-picks']))
print("\t* Stake: " + str(formula['stake']))
print("\t* Yield: " + str(formula['yield']) + " %")
print("\t* Detall per mesos:\n")

for periodName, periodData in formula['periods'].items():
    try:
        print("\t\t-> " + periodName + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tStake " + str(periodData['stake']) + "\tYield: " + str(periodData['yield']) + " %")
    except:
        print("\t\t-> " + periodName + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: 0.00 %")

#printArray(formula['games'])
