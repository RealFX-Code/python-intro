import matplotlib
# Install Pyqt6!
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import random
import country_converter as coco
import copy

# Init so python knows this should be global
data = {}

def parse_csv():
    with open("average-annual-surface-temperature.csv", "r") as f:
        for row in csv.reader(f):
            # Skip the headers
            if row[0] != "Entity":
                if not row[0] in data:
                    data[row[0]] = []
                data[row[0]].append({ "year": row[2], "temp": row[3]})

def plot_year(country, color):
    years = []
    temps = []

    for datacountry in data:
        if datacountry.lower() == country.lower():
            for row in data[datacountry]:
                temps.append(float(row["temp"]))
                years.append(int(row["year"]))

    yaxis = np.array(temps)
    xaxis = np.array(years)
    plt.plot(xaxis, yaxis, color)

def plot_all():
    colors_done = []
    color = ""
    for datacountry in data:
        years = []
        temps = []
        for row in data[datacountry]:
            temps.append(float(row["temp"]))
            years.append(int(row["year"]))
        yaxis = np.array(temps)
        xaxis = np.array(years)
        while True:
            # 3 random hex numbers for a random hex color code
            color = f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"
            if color not in colors_done:
                colors_done.append(color)
                break
        plt.plot(xaxis, yaxis, color)
    plt.xlabel("Year")
    plt.ylabel("Temperature")

def plot_continents():
    # Data structure:

    # temps = {
    #   "Asia": {
    #       "1940" : [
    #           10.00498,
    #           9.7742
    #           ...    
    #       ]
    #   }
    # }
    #
    # avgtemps = {
    #   "Asia": [
    #       10.49832 # for 1940
    #       10.8847 # for 1942
    #   ]
    # }
    #
    # Years is just an array of the years we have.
    temps = {}
    avgtemps = {}
    years = []
    # For each country we have data from
    for datacountry in data:
        cc = coco.CountryConverter()
        continent = cc.convert(datacountry, to="Continent")
        if continent == "not found":
            continue
    
        if not continent in temps:
            temps[continent] = {}
            avgtemps[continent] = []

        for row in data[datacountry]:
            if not row["year"] in temps[continent]:
                temps[continent][row["year"]] = []
            # datacountry = Afghanistan
            # data[datacountry] == {"year": "1940", "temp": "0.994876"}
            # This somehow works, pls don't touch
            temps[continent][row["year"]].append(float(row["temp"]))

            # Should only be to add the years on the first loop
            if int(row["year"]) not in years:
                years.append(int(row["year"]))
    for continent in temps:
        avg = float(0)
        amt = float(0)
        for year in temps[continent]:
            for temp in temps[continent][year]:
                avg += temp
                amt += 1
            avgtemps[continent].append(avg / amt)
    colors = plt.cm.tab10(np.linspace(0, 1, len(temps)))
    for continent, color in zip(temps, colors):
        # We should always have one data point for each year.
        assert len(avgtemps[continent]) == len(years)

        yaxis = np.array(avgtemps[continent])
        xaxis = np.array(years)
        plt.plot(xaxis, yaxis, color=color, label=continent)
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Temperature")
    plt.show()

def main():
    parse_csv()
    plot_continents()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
