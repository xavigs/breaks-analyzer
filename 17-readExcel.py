import openpyxl

def printArray(data):
    print("[")

    for element in data:
        print("\t{")

        for key in element:
            print("\t\t'" + str(key) + "': " + str(element[key]))

        print("\t}")

    print("]")

# Variables
games = []
date = ""

# Parameters
parameters = []
parameter = {}
parameter['key'] = "probability"
parameter['comparator'] = ">="
parameter['condition'] = 0.9
parameter['type'] = "number"
parameters.append(parameter)
parameter = {}
parameter['key'] = "value"
parameter['comparator'] = ">="
parameter['condition'] = 1.6
parameter['type'] = "number"
parameters.append(parameter)
parameter = {}
parameter['key'] = "home"
parameter['comparator'] = "="
parameter['condition'] = "SN"
parameter['type'] = "text"
parameters.append(parameter)
parameter = {}
parameter['key'] = "odd"
parameter['comparator'] = ">"
parameter['condition'] = 2.0
parameter['type'] = "number"
parameters.append(parameter)
parameter = {}
parameter['key'] = "opponent_odd"
parameter['comparator'] = "<"
parameter['condition'] = 1.2
parameter['type'] = "number"
parameters.append(parameter)
parameter = {}
parameter['key'] = "category"
parameter['comparator'] = "="
parameter['condition'] = "ITF"
parameter['type'] = "text"
parameters.append(parameter)
parameter = {}
parameter['key'] = "last"
parameter['comparator'] = "="
parameter['condition'] = "OK"
parameter['type'] = "text"
parameters.append(parameter)
numParams = len(parameters)
combinations = ["01-03", "01-04", "01-05", "01-12", "01-14", "01-15", "01-16", "01-23", "01-24", "01-25", "01-26", "01-34", "01-36", "01-46", "01-56", "03-04", "03-12", "03-14", "03-15", "03-16", "03-23", "03-24", "03-25", "03-26", "03-34", "03-36", "03-46", "03-56", "04-12", "04-14", "04-15", "04-16", "04-23", "04-24", "04-25", "04-26", "04-34", "04-36", "04-46", "04-56", "12-14", "12-15", "12-16", "12-23", "12-24", "12-25", "12-26", "12-34", "12-36", "12-46", "12-56", "14-15", "14-16", "14-23", "14-24", "14-25", "14-26", "14-34", "14-36", "14-46", "14-56", "15-16", "15-23", "15-24", "15-25", "15-26", "15-34", "15-36", "15-46", "15-56", "16-23", "16-24", "16-25", "16-26", "16-34", "16-36", "16-46", "16-56", "23-24", "23-25", "23-26", "23-34", "23-36", "23-46", "23-56", "24-25", "24-26", "24-34", "24-36", "24-46", "24-56", "25-26", "25-34", "25-36", "25-46", "25-56", "26-34", "26-36", "26-46", "26-56", "34-36", "34-46", "34-56", "36-46", "36-56", "46-56" ]

# Open Workbook
wb = openpyxl.load_workbook (filename = "Breaks 1r set.xlsx", read_only = True)

# Get Sheet Object by names
o_sheet = wb.get_sheet_by_name ( "Break" )

for row in range ( 4, 5264 ):
    if row != 162 and row != 1352:
        # Create game object
        game = {}

        # Get Cell Values
        game['surface'] = o_sheet['D' + str(row)].value
        game['player'] = o_sheet['E' + str(row)].value
        game['opponent'] = o_sheet['F' + str(row)].value
        game['opponent_odd'] = o_sheet['H' + str(row)].value
        game['odd'] = o_sheet['K' + str(row)].value
        game['probability'] = o_sheet['L' + str(row)].value
        game['value'] = o_sheet['N' + str(row)].value
        game['result'] = o_sheet['O' + str(row)].value

        # Date
        if o_sheet['A' + str(row)].value != None:
            date = o_sheet['A' + str(row)].value

        game['date'] = date

        # ATP o WTA
        if o_sheet['B' + str(row)].value == "WTA":
            game['sex'] = "W"
        else:
            game['sex'] = "M"

        # ITF o Altres
        if o_sheet['B' + str(row)].value == "ITF" or o_sheet['C' + str(row)].value == "ITF":
            game['category'] = "ITF"
        else:
            game['category'] = "Other"

        # Last
        if o_sheet['G' + str(row)].value == "OK":
            last = "OK"
        else:
            last = "NO"

        game['last'] = last

        # Home/Away
        game['home'] = o_sheet['I' + str(row)].value + o_sheet['J' + str(row)].value

        # Balance
        if game['result'] == "L":
            game['balance'] = -1
        elif game['result'] == "N":
            game['balance'] = 0
        else:
            game['balance'] = game['odd'] - 1

        # Add game to array
        games.append(game)

# Calculate balance by parameters
'''systems = []

for index1 in range ( 0, numParams ):
    for index2 in range ( index1 + 1, numParams ):
        system = {}
        system['condition'] = parameters[index1]['key'] + " " + parameters[index1]['comparator'] + " " + str ( parameters[index1]['condition'] ) + " AND " + parameters[index2]['key'] + " " + parameters[index2]['comparator'] + " " + str ( parameters[index2]['condition'] )
        balance = {}
        balance['picks'] = 0
        balance['units'] = 0.0

        for game in games:
            condition1 = False
            condition2 = False

            # Condition 1
            if parameters[index1]['type'] == "text":
                # Text
                if parameters[index1]['comparator'] == "=":
                    if game[parameters[index1]['key']] == parameters[index1]['condition']:
                        condition1 = True
                else:
                    if game[parameters[index1]['key']] != parameters[index1]['condition']:
                        condition1 = True
            else:
                # Number
                if parameters[index1]['comparator'] == ">":
                    if game[parameters[index1]['key']] > parameters[index1]['condition']:
                        condition1 = True
                elif parameters[index1]['comparator'] == ">=":
                    if game[parameters[index1]['key']] >= parameters[index1]['condition']:
                        condition1 = True
                elif parameters[index1]['comparator'] == "<":
                    if game[parameters[index1]['key']] < parameters[index1]['condition']:
                        condition1 = True
                else:
                    if game[parameters[index1]['key']] <= parameters[index1]['condition']:
                        condition1 = True

            # Condition 2
            if condition1:
                if parameters[index2]['type'] == "text":
                    # Text
                    if parameters[index2]['comparator'] == "=":
                        if game[parameters[index2]['key']] == parameters[index2]['condition']:
                            condition2 = True
                    else:
                        if game[parameters[index2]['key']] != parameters[index2]['condition']:
                            condition2 = True
                else:
                    # Number
                    if parameters[index2]['comparator'] == ">":
                        if game[parameters[index2]['key']] > parameters[index2]['condition']:
                            condition2 = True
                    elif parameters[index2]['comparator'] == ">=":
                        if game[parameters[index2]['key']] >= parameters[index2]['condition']:
                            condition2 = True
                    elif parameters[index2]['comparator'] == "<":
                        if game[parameters[index2]['key']] < parameters[index2]['condition']:
                            condition2 = True
                    else:
                        if game[parameters[index2]['key']] <= parameters[index2]['condition']:
                            condition2 = True

            if condition1 and condition2:
                balance['picks'] += 1
                balance['units'] += game['balance']

        if balance['picks'] > 0:
            balance['yield'] = round ( balance['units'] * 100 / balance['picks'], 2 )
            system['balance'] = balance
            systems.append(system)'''

# Calculate balance by combinations
systems = []

for combination in combinations:
    index1 = int(combination[0:1])
    index2 = int(combination[1:2])
    index3 = int(combination[3:4])
    index4 = int(combination[4:5])
    system = {}
    system['condition'] = parameters[index1]['key'] + " " + parameters[index1]['comparator'] + " " + str ( parameters[index1]['condition'] ) + " + " + parameters[index2]['key'] + " " + parameters[index2]['comparator'] + " " + str ( parameters[index2]['condition'] ) + " OR " + parameters[index3]['key'] + " " + parameters[index3]['comparator'] + " " + str ( parameters[index3]['condition'] ) + " + " + parameters[index4]['key'] + " " + parameters[index4]['comparator'] + " " + str ( parameters[index4]['condition'] )
    balance = {}
    balance['picks'] = 0
    balance['units'] = 0.0

    for game in games:
        condition1 = False
        condition2 = False
        condition3 = False
        condition4 = False

        # Condition 1
        if parameters[index1]['type'] == "text":
            # Text
            if parameters[index1]['comparator'] == "=":
                if game[parameters[index1]['key']] == parameters[index1]['condition']:
                    condition1 = True
            else:
                if game[parameters[index1]['key']] != parameters[index1]['condition']:
                    condition1 = True
        else:
            # Number
            if parameters[index1]['comparator'] == ">":
                if game[parameters[index1]['key']] > parameters[index1]['condition']:
                    condition1 = True
            elif parameters[index1]['comparator'] == ">=":
                if game[parameters[index1]['key']] >= parameters[index1]['condition']:
                    condition1 = True
            elif parameters[index1]['comparator'] == "<":
                if game[parameters[index1]['key']] < parameters[index1]['condition']:
                    condition1 = True
            else:
                if game[parameters[index1]['key']] <= parameters[index1]['condition']:
                    condition1 = True

        # Condition 2
        if condition1:
            if parameters[index2]['type'] == "text":
                # Text
                if parameters[index2]['comparator'] == "=":
                    if game[parameters[index2]['key']] == parameters[index2]['condition']:
                        condition2 = True
                else:
                    if game[parameters[index2]['key']] != parameters[index2]['condition']:
                        condition2 = True
            else:
                # Number
                if parameters[index2]['comparator'] == ">":
                    if game[parameters[index2]['key']] > parameters[index2]['condition']:
                        condition2 = True
                elif parameters[index2]['comparator'] == ">=":
                    if game[parameters[index2]['key']] >= parameters[index2]['condition']:
                        condition2 = True
                elif parameters[index2]['comparator'] == "<":
                    if game[parameters[index2]['key']] < parameters[index2]['condition']:
                        condition2 = True
                else:
                    if game[parameters[index2]['key']] <= parameters[index2]['condition']:
                        condition2 = True

        if not condition1 or not condition2:
            # Condition 3
            if parameters[index3]['type'] == "text":
                # Text
                if parameters[index3]['comparator'] == "=":
                    if game[parameters[index3]['key']] == parameters[index3]['condition']:
                        condition3 = True
                else:
                    if game[parameters[index3]['key']] != parameters[index3]['condition']:
                        condition3 = True
            else:
                # Number
                if parameters[index3]['comparator'] == ">":
                    if game[parameters[index3]['key']] > parameters[index3]['condition']:
                        condition3 = True
                elif parameters[index3]['comparator'] == ">=":
                    if game[parameters[index3]['key']] >= parameters[index3]['condition']:
                        condition3 = True
                elif parameters[index3]['comparator'] == "<":
                    if game[parameters[index3]['key']] < parameters[index3]['condition']:
                        condition3 = True
                else:
                    if game[parameters[index3]['key']] <= parameters[index3]['condition']:
                        condition3 = True

            # Condition 4
            if condition3:
                if parameters[index4]['type'] == "text":
                    # Text
                    if parameters[index4]['comparator'] == "=":
                        if game[parameters[index4]['key']] == parameters[index4]['condition']:
                            condition4 = True
                    else:
                        if game[parameters[index4]['key']] != parameters[index4]['condition']:
                            condition4 = True
                else:
                    # Number
                    if parameters[index4]['comparator'] == ">":
                        if game[parameters[index4]['key']] > parameters[index4]['condition']:
                            condition4 = True
                    elif parameters[index4]['comparator'] == ">=":
                        if game[parameters[index4]['key']] >= parameters[index4]['condition']:
                            condition4 = True
                    elif parameters[index4]['comparator'] == "<":
                        if game[parameters[index4]['key']] < parameters[index4]['condition']:
                            condition4 = True
                    else:
                        if game[parameters[index4]['key']] <= parameters[index4]['condition']:
                            condition4 = True

        if condition1 and condition2 or condition3 and condition4:
            balance['picks'] += 1
            balance['units'] += game['balance']

    if balance['picks'] > 74:
        balance['units'] = round ( balance['units'], 2 )
        balance['yield'] = round ( balance['units'] * 100 / balance['picks'], 2 )
        system['balance'] = balance

        if balance['yield'] > 20.0:
            balance['yield'] = str ( balance['yield'] ) + "%"
            systems.append(system)

printArray(systems)
