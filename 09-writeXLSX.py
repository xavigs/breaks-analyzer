import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from os.path import *
from datetime import datetime

dayString = "2022-02-08"
filepath = "{}.xlsx".format(dayString)

if isfile(filepath):
    wb = openpyxl.load_workbook(filepath)
else:
    wb = openpyxl.Workbook()

fontRegularBlack = Font(
    name = "Arial",
    size = 10,
    bold = False
)
fontBoldBlack = Font(
    name = "Arial",
    size = 10,
    bold = True
)
fontRegularWhite = Font(
    name = "Arial",
    size = 10,
    bold = False,
    color = "ffffff"
)
alignmentLeft = Alignment(
    horizontal = "left",
    vertical = "center"
)
alignmentCenter = Alignment(
    horizontal = "center",
    vertical = "center"
)
rightBorder = Border(
    right = Side(style="thin")
)

ws = wb.active
ws.title = "Daily"
day = datetime.strptime(dayString, "%Y-%m-%d")
ws['A1'] = day
ws['A1'].number_format = "dd-MMM"
ws['A1'].font = fontBoldBlack
ws['A1'].alignment = alignmentCenter
ws['A1'].border = rightBorder
ws['A1'].fill = PatternFill(start_color = "ffd966", end_color = "ffd966", fill_type = "solid")
ws['B1'] = "ATP"
ws['B1'].font = fontRegularBlack
ws['B1'].alignment = alignmentCenter
ws['B1'].fill = PatternFill(start_color = "ccccdd", end_color = "ccccdd", fill_type = "solid")
ws['C1'] = 500
ws['C1'].font = fontRegularBlack
ws['C1'].alignment = alignmentCenter
ws['C1'].fill = PatternFill(start_color = "ccccdd", end_color = "ccccdd", fill_type = "solid")
ws['D1'] = "I"
ws['D1'].font = fontRegularWhite
ws['D1'].alignment = alignmentCenter
ws['D1'].fill = PatternFill(start_color = "618cb1", end_color = "618cb1", fill_type = "solid")
ws['E1'] = "Text1"
ws['E1'].font = fontBoldBlack
ws['E1'].alignment = alignmentLeft
ws['F1'] = "Text2"
ws['F1'].font = fontRegularBlack
ws['F1'].alignment = alignmentLeft
ws['G1'] = "OK"
ws['G1'].font = fontRegularWhite
ws['G1'].alignment = alignmentCenter
ws['G1'].fill = PatternFill(start_color = "34a853", end_color = "34a853", fill_type = "solid")
ws['H1'] = 1.61
ws['H1'].font = fontRegularBlack
ws['H1'].alignment = alignmentCenter
ws['I1'] = "N"
ws['I1'].font = fontRegularWhite
ws['I1'].alignment = alignmentCenter
ws['I1'].fill = PatternFill(start_color = "ee0000", end_color = "ee0000", fill_type = "solid")
ws['J1'] = "S"
ws['J1'].font = fontRegularWhite
ws['J1'].alignment = alignmentCenter
ws['J1'].fill = PatternFill(start_color = "ee0000", end_color = "ee0000", fill_type = "solid")
ws['K1'] = 1.66
ws['K1'].font = fontRegularBlack
ws['K1'].alignment = alignmentCenter
ws['L1'].value = "74,50%"
ws['L1'].number_format = "0.00%"
ws['L1'].font = fontBoldBlack
ws['L1'].alignment = alignmentCenter
ws['M1'].value = "=1/K1" # 62,11%
ws['M1'].number_format = "0.00%"
ws['M1'].font = fontRegularBlack
ws['M1'].alignment = alignmentCenter
ws['N1'] = "=L1/M1"
ws['N1'].font = fontBoldBlack
ws['N1'].alignment = alignmentCenter
ws['N1'].number_format = "#,##0.00"
ws['B1'].border = rightBorder
ws['B2'] = "CH"
ws['B2'].font = fontRegularWhite
ws['B2'].alignment = alignmentCenter
ws['B2'].fill = PatternFill(start_color = "53a01d", end_color = "53a01d", fill_type = "solid")
ws.merge_cells('B2:C2')
ws['D2'] = "D"
ws['D2'].font = fontRegularWhite
ws['D2'].alignment = alignmentCenter
ws['D2'].fill = PatternFill(start_color = "788575", end_color = "788575", fill_type = "solid")
ws['E2'] = "Text3"
ws['E2'].font = fontBoldBlack
ws['E2'].alignment = alignmentLeft
ws['F2'] = "Text4"
ws['F2'].font = fontRegularBlack
ws['F2'].alignment = alignmentLeft
ws['G2'] = "10"
ws['G2'].font = fontRegularBlack
ws['G2'].alignment = alignmentCenter
ws['H2'] = 1.61
ws['H2'].font = fontRegularBlack
ws['H2'].alignment = alignmentCenter
ws['I2'] = "S"
ws['I2'].font = fontRegularWhite
ws['I2'].alignment = alignmentCenter
ws['I2'].fill = PatternFill(start_color = "34a853", end_color = "34a853", fill_type = "solid")
ws['J2'] = "N"
ws['J2'].font = fontRegularWhite
ws['J2'].alignment = alignmentCenter
ws['J2'].fill = PatternFill(start_color = "34a853", end_color = "34a853", fill_type = "solid")
ws['K2'] = 1.66
ws['K2'].font = fontRegularBlack
ws['K2'].alignment = alignmentCenter
ws['L2'].value = "74,50%"
ws['L2'].number_format = "0.00%"
ws['L2'].font = fontBoldBlack
ws['L2'].alignment = alignmentCenter
ws['M2'].value = "=1/K1" # 62,11%
ws['M2'].number_format = "0.00%"
ws['M2'].font = fontRegularBlack
ws['M2'].alignment = alignmentCenter
ws['N2'] = "=L1/M1"
ws['N2'].font = fontBoldBlack
ws['N2'].alignment = alignmentCenter
ws['N2'].number_format = "#,##0.00"
ws.merge_cells('A1:A2')
wb.save(filepath)

'''
    # TODO DB

    1) Collection tournament (teID)
    2) Save tournament data: teID (_id), teName, sex, category, surface
    3) Into game documents, new fields: tournament (teID), time
    4) Into player lastGames (or game documents), newField: last ("OK", "01", "02", "10", "11", "12", "20", "21", "22")
    5) Tractament d'excepcions a tots els scripts, perquè es generi un log, però no deixi de funcionar quan un element falla
'''
