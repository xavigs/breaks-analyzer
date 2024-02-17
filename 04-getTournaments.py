# -*- coding: utf-8 -*-
from datetime import date
import click
from utils import *
import tennisExplorer
import itfTennis
from models import db, objects

dbConnection = db.Database()
breaksDB = dbConnection.connect()
tournamentsObj = objects.Tournaments(breaksDB)

@click.command()
@click.option(
    '-s', '--sex',
    help = "Sex category to get tournaments from", type = str, default = "M", show_default = True
)
@click.option(
    '-y', '--year',
    help = "Year to get tournaments from", type = str, default = date.today().year, show_default = True
)

def getYearlyTournaments(sex, year):
    tournamentsObj.delete([{'sex': sex}])
    print("# Getting tournaments from Tennis Explorer...")
    tournaments = tennisExplorer.getTournaments(sex, year)
    print("# Getting tournaments from ITF Tennis...")
    tournaments += itfTennis.getTournaments(sex, year)
    print("# Inserting tournaments into the DB...")

    for tournament in tournaments:
        tournamentsObj.create(tournament)

if __name__ == '__main__':
    getYearlyTournaments()
