# -*- coding: utf-8 -*-
import sys
import openpyxl
import json

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
    "Sistema 1",
    "Sistema 3",
    "Sistema NAS",
    "Sistema JUAS",
    "Sistema D1SITIS",
    "Sistema JIXTA",
    "Sistema Experimental",
    "Sistema Experimental I",
    "Sistema Experimental II",
    "Sistema Experimental III",
    "Sistema Experimental IV",
    "Sistema Experimental V",
    "Sistema Experimental VI",
    "Sistema Experimental VII",
    "Sistema Experimental VIII",
    "Sistema Experimental IX",
    "Sistema Experimental X"
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
    systems[system['name']]['units'] = 0.0
    systems[system['name']]['num-picks'] = 0
    systems[system['name']]['total-months'] = 0
    systems[system['name']]['positive-months'] = 0
    systems[system['name']]['10plus-months'] = 0
    systems[system['name']]['periods'] = {}

    if "future" in system:
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
workbook = openpyxl.load_workbook(filename = "Breaks 1r set.xlsx", data_only = True)

# Get Sheet Object by names
sheet = workbook['Break']

for row in range(4, parameters['last-row'] + 1):
    if sheet['A' + str(row)].value is not None:
        date = sheet['A' + str(row)].value

    if not row in parameters['jump']:
        valid = True

        for criteria in parameters['dismiss']:
            if criteria['operator'] == "=":
                if sheet[criteria['col'] + str(row)].value == criteria['value']:
                    valid = False
                    break
            elif criteria['operator'] == "<":
                if sheet[criteria['col'] + str(row)].value < criteria['value']:
                    valid = False
                    break
            elif criteria['operator'] == ">":
                if sheet[criteria['col'] + str(row)].value > criteria['value']:
                    valid = False
                    break
            elif criteria['operator'] == ">=":
                if sheet[criteria['col'] + str(row)].value >= criteria['value']:
                    valid = False
                    break
            elif criteria['operator'] == "<>":
                if sheet[criteria['col'] + str(row)].value != criteria['value']:
                    valid = False
                    break

        #if valid or not valid:
        if valid:
            found = False

            for system in parameters['systems']:
                validForSystem = False

                for conditionGroup in system['conditions']:
                    numConditions = len(conditionGroup)
                    satisfiedConditions = 0

                    for condition in conditionGroup:
                        if condition['operator'] == "=":
                            if sheet[condition['col'] + str(row)].value == condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == "<":
                            if sheet[condition['col'] + str(row)].value < condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == ">":
                            if sheet[condition['col'] + str(row)].value > condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == ">=":
                            if sheet[condition['col'] + str(row)].value >= condition['value']:
                                satisfiedConditions += 1
                        elif condition['operator'] == "<>":
                            if sheet[condition['col'] + str(row)].value != condition['value']:
                                satisfiedConditions += 1

                    if numConditions == satisfiedConditions:
                        validForSystem = True
                        break

                if validForSystem:
                    game = {}
                    game['date'] = date
                    game['player'] = sheet['E' + str(row)].value
                    game['opponent'] = sheet['F' + str(row)].value
                    game['odd'] = sheet['K' + str(row)].value
                    game['result'] = sheet['O' + str(row)].value

                    # Balance
                    if sheet['O' + str(row)].value == "L":
                        balance = -1
                    elif sheet['O' + str(row)].value == "N":
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

                    if "future" in system and row >= system['future']:
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
                                if row >= period['first-row'] and row <= period['last-row'] and period['type'] == 1:
                                    formula['periods'][period['keyword']]['units'] += balance * formulaSystem['stake']
                                    formula['periods'][period['keyword']]['num-picks'] += 1
                                    formula['periods'][period['keyword']]['stake'] += formulaSystem['stake']
                                    formula['periods'][period['keyword']]['yield'] = round(formula['periods'][period['keyword']]['units'] * 100 / formula['periods'][period['keyword']]['stake'], 2)

                    for period in parameters['periods']:
                        if row >= period['first-row'] and row <= period['last-row']:
                            systems[system['name']]['periods'][period['keyword']]['units'] += balance
                            systems[system['name']]['periods'][period['keyword']]['num-picks'] += 1
                            systems[system['name']]['periods'][period['keyword']]['yield'] = round(systems[system['name']]['periods'][period['keyword']]['units'] * 100 / systems[system['name']]['periods'][period['keyword']]['num-picks'], 2)

for systemName, systemData in sorted(systems.items()):
    if "Sistema" in systemName:
        systemName = systemName.split("-")[1]
        print("\n~~ " + systemName + " ~~\n")
        print("\t* Unitats: " + str(round(systemData['units'],2)) + " uts.")
        print("\t* N?? picks: " + str(systemData['num-picks']))
        print("\t* Yield: " + str(systemData['yield']) + " %")
        positiveMonths = 0
        plusMonths = 0

        for period in systemData['periods']:
            if systemData['periods'][period]['type'] == 1 and systemData['periods'][period]['units'] > 0:
                positiveMonths += 1

                if systemData['periods'][period]['yield'] >= 10:
                    plusMonths += 1

        print("\t* Mesos positius: " + str(positiveMonths))
        print("\t* Mesos amb m??s del 10% de yield: " + str(plusMonths))
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
                    stake = round(bank / 40, 2)
                except:
                    print("\t\t-> " + periodData['name'] + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: 0.00 %")

        if "future" in systemData:
            print("\n\t* Dades futures:\n")
            print("\t\t-> Unitats: " + str(round(systemData['future']['units'],2)) + " uts.")
            print("\t\t-> N?? picks: " + str(systemData['future']['num-picks']))
            print("\t\t-> Yield: " + str(systemData['future']['yield']) + " %")

#exit()
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

sys.stdout.write("\n| N?? picks |")

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
sys.stdout.write("\n")
exit()
print("\n\n~~ F??rmula Actual ~~\n")
print("\t* Unitats: " + str(round(formula['units'],2)) + " uts.")
print("\t* N?? picks: " + str(formula['num-picks']))
print("\t* Stake: " + str(formula['stake']))
print("\t* Yield: " + str(formula['yield']) + " %")
print("\t* Detall per mesos:\n")

for periodName, periodData in formula['periods'].items():
    try:
        print("\t\t-> " + periodName + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tStake " + str(periodData['stake']) + "\tYield: " + str(periodData['yield']) + " %")
    except:
        print("\t\t-> " + periodName + "\t" + str(round(periodData['units'], 2)) + " uts.\t" + str(periodData['num-picks']) + " picks \tYield: 0.00 %")

#printArray(formula['games'])
