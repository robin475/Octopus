import csv
import datetime
import time
import calendar
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import math
from matplotlib.figure import Figure
from flask import Flask, render_template, request
from io import BytesIO
import base64


csv.register_dialect('octopus', delimiter=',', skipinitialspace=True)

with open('consumption.csv', 'r') as file:
    CSreader = csv.DictReader(file, delimiter = ',', skipinitialspace=True)


    def hourlyAvgBD():
#        import pdb; pdb.set_trace()
        dayTotals = []
        dayTotal = 0
        yesterday = 1
        dayNumbers = []
        hourlyAverages = []
        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))

            if date.day != yesterday:
                dayTotals.append(round(dayTotal,3))
                hourlyAverage = dayTotal / 24
                hourlyAverages.append(hourlyAverage)
                
                dayTotal = 0
                dayNumbers.append(dayDate.strftime("%d/%m/%y"))
                
            dayTotal += float(row.get('Consumption (kWh)', 0))      
            yesterday = date.day
            dayDate = date
        dayTotals.append(round(dayTotal,3))
        dayNumbers.append(date.strftime("%d/%m/%y"))
        hourlyAverages.append(round(dayTotal,3))
        print(dayTotals)
        dataToAdd = {'Date': dayNumbers, 'Hourly Average': hourlyAverages}
        df = pd.DataFrame(dataToAdd) # gather data
        df = df.set_index(df['Date'])
        df.plot()
        plt.show()
        print(df) 

    def monthlyAvgs():
        monthAverages = []
        monthNumbers = []
        monthTotal = 0
        lastMonth = 1
        daysInMonth = 0


        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))

            if date.month != lastMonth:
                monthAvg = monthTotal / daysInMonth
                monthAverages.append(round(monthAvg, 3))
                monthNumbers.append(monthDate.strftime("%m/%y"))
                monthTotal = 0
                
            monthTotal += float(row.get('Consumption (kWh)', 0))      
            lastMonth = date.month
            daysInMonth = date.day
            monthDate = date

        daysInMonth = date.day
        monthAvg = monthTotal / daysInMonth
        monthAverages.append(round(monthAvg,3))
        monthNumbers.append(date.strftime("%m/%y"))

        print(monthNumbers)
        print(monthAverages)
        plt.figure(figsize=(24,8))
        plt.title("Average daily power consumption by month")
        plt.xlabel("Months")
        plt.ylabel("Average Daily Consumption (kWh)")
        
        
        plt.plot(monthNumbers, monthAverages, 'X-b')
        plt.show()

    def hourlyAvgBM():
        preHour = 0
        hourTotal = 0
        timer = []
        df = pd.DataFrame()
        
        for i in range(0,24):
            timer.append(0)
        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))
            if date.hour != preHour:
                timer[preHour] = float(timer[preHour]) + hourTotal
                
                hourTotal = 0

                if date.month != lastMonth:
                    for i in range(0,24):
                        timer[i] = timer[i] / lastDate.day
                
                    if lastDate.strftime("%b") in df:
                        current = df[lastDate.strftime("%b")]
                        current = current.to_numpy()
                        for i in range(0, len(current)):
                            timer[i] = (timer[i] + current[i])/2
                            

                        #take correct array from dataframe and average each one (/2)

                    df[lastDate.strftime("%b")] = timer
                    for i in range(0,24):
                        timer[i] = 0             
                
            hourTotal += float(row.get('Consumption (kWh)', 0))      
            preHour = date.hour
            lastMonth = date.month
            lastDate = date
        for i in range(0, len(timer)):
            timer[i] = round(timer[i],3)
        print(df)
        df.plot.line(figsize=(24,8), title = "Average Hourly Consumption by Month", xlabel = "Time (Hours)", ylabel = "Consumption (kWh)")        
 
        plt.show()

    def monthlyAggs():
        monthAggregates = []
        monthNumbers = []
        monthTotal = 0
        lastMonth = 1
        daysInMonth = 0
        

        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))

            if date.month != lastMonth:
                monthTotalkw = monthTotal * daysInMonth * 24
                monthAggregates.append(round(monthTotalkw, 3))
                monthNumbers.append(monthDate.strftime("%m/%y"))
                monthTotal = 0


            monthTotal += float(row.get('Consumption (kWh)', 0))      
            lastMonth = date.month
            daysInMonth = date.day
            monthDate = date

        daysInMonth = date.day
        monthTotalkw = monthTotal * daysInMonth * 24
        monthAggregates.append(round(monthTotalkw,3))
        monthNumbers.append(date.strftime("%m/%y"))
        dataADDED = {'Months': monthNumbers,'Consumed': monthAggregates}
        df = pd.DataFrame(data=dataADDED)
        print(df)
        plt.figure(figsize=(24,8))
        plt.bar(df['Months'],df['Consumed'])

        def rounder(num, dp):
            multi = 10 ** dp
            return math.ceil(num * multi) / multi
        monthAggregates.sort(reverse=True)
        top = rounder(monthAggregates[0],-5)
        axes = plt.gca()
        axes.set_ylim([0,top])
        plt.title("Aggregate Monthly Energy Consumption")
        plt.xlabel("Months")
        plt.ylabel("Consumption (kW)")
        plt.show()

    def daysOfTheWeek():
        preHour = 0
        hourTotal = 0
        timer = []
        df = pd.DataFrame()
        whatDay = []
        for i in range(0,24):
            timer.append(0)
        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))
            if date.hour != preHour:
                timer[preHour] = float(timer[preHour]) + hourTotal
                
                hourTotal = 0

                if date.weekday() != yesterday:
                    whatDay.append(date.weekday())
                    if lastDate.strftime("%a") in df:
                        current = df[lastDate.strftime("%a")]
                        current = current.to_numpy()
                        for i in range(0, len(current)):
                            timer[i] = timer[i] + current[i]
                            

                    df[lastDate.strftime("%a")] = timer
                    for i in range(0,24):
                        timer[i] = 0             
                
            hourTotal += float(row.get('Consumption (kWh)', 0))      
            preHour = date.hour
            yesterday = date.weekday()
            lastDate = date
        print(whatDay)
        dayCount = 0
        for i in range(0,len(whatDay)):
            if whatDay[i] == 0:
                dayCount += 1
        print(dayCount)
        names = df.columns
        for i in range(0, len(names)):
            colm = df[names[i]]
            colm = colm.to_numpy()
            for j in range(0, len(colm)):
                colm[j] = colm[j] / 83 
            df[names[i]] = colm


        print(df)
        df.plot.line(figsize=(24,8), title = "Average Hourly Consumption by Weekday", xlabel = "Time (Hours)", ylabel = "Consumption (kWh)")        
 
        plt.show()

    def heatMappage():    ##doesnt work fix fix fix
        preHour = 0
        hourTotal = 0
        timer = []
        df = pd.DataFrame()
        whatDay = []
        for i in range(0,24):
            timer.append(0)
        for row in CSreader:
            date = datetime.datetime.fromisoformat(row.get('Start',0))
            if date.hour != preHour:
                timer[preHour] = float(timer[preHour]) + hourTotal
                
                hourTotal = 0

                if date.weekday() != yesterday:
                    whatDay.append(date.weekday())
                    if lastDate.strftime("%a") in df:
                        current = df[lastDate.strftime("%a")]
                        current = current.to_numpy()
                        for i in range(0, len(current)):
                            timer[i] = timer[i] + current[i]
                            

                    df[lastDate.strftime("%a")] = timer
                    for i in range(0,24):
                        timer[i] = 0             
                
            hourTotal += float(row.get('Consumption (kWh)', 0))      
            preHour = date.hour
            yesterday = date.weekday()
            lastDate = date
        dayCount = 0
        for i in range(0,len(whatDay)):
            if whatDay[i] == 0:
                dayCount += 1
        names = df.columns
        for i in range(0, len(names)):
            colm = df[names[i]]
            colm = colm.to_numpy()
            for j in range(0, len(colm)):
                colm[j] = colm[j] / dayCount
            df[names[i]] = colm   
             
        print(df)
        plt.imshow(df) 
        plt.xticks(range(len(df)), df.index)
        plt.yticks(range(len(df)), df.columns)



        plt.show()



#    hourlyAvgBD()
#    monthlyAvgs()
#    hourlyAvgBM()
#    monthlyAggs()
#    daysOfTheWeek()
#    heatMappage()



app = Flask(__name__)  
with app.app_context(): 

    
    @app.route('/hello')
    def hello():
        return 'HELLO EVERYBODY'

    @app.route('/graph')
    def graph():
        fig = Figure()
        ax = fig.subplots()
        ax.plot([1, 2])
    # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
    # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
    

    @app.route('/monthly', methods = ["GET", "POST"])
    def hourlyMonthly():
        csv.register_dialect('octopus', delimiter=',', skipinitialspace=True)

        with open('consumption.csv', 'r') as file:
            CSreader = csv.DictReader(file, delimiter = ',', skipinitialspace=True)
            try:
                if request.method == "POST":
                    startDatehtml = request.form.get("dater1")
                    print(startDatehtml)
                    endDatehtml = request.form.get("dater2")
                    print(endDatehtml)

                startDate = time.strptime(startDatehtml, "%Y-%m-%d")
                endDate = time.strptime(endDatehtml, "%Y-%m-%d")
            except UnboundLocalError:
                startDate = time.strptime("2023-01-01", "%Y-%m-%d")
                endDate = time.strptime("2024-08-04", "%Y-%m-%d")


            preHour = 0
            hourTotal = 0
            timer = []
            df = pd.DataFrame()
            
            for i in range(0,24):
                timer.append(0)

            beacon = 0
            for row in CSreader:
                date = datetime.datetime.fromisoformat(row.get('Start',0))
                dateCHECK = date.strftime("%Y-%m-%d")
                testDate = time.strptime(str(dateCHECK), "%Y-%m-%d")
                if testDate > startDate and testDate < endDate:
                    if date.hour != preHour:
                        timer[preHour] = float(timer[preHour]) + hourTotal
                        
                        hourTotal = 0

                        if date.month != lastMonth:
                            for i in range(0,24):
                                timer[i] = timer[i] / lastDate.day
                        
                            if lastDate.strftime("%b") in df:
                                current = df[lastDate.strftime("%b")]
                                current = current.to_numpy()
                                for i in range(0, len(current)):
                                    timer[i] = (timer[i] + current[i])/2
                                    

                                #take correct array from dataframe and average each one (/2)

                            df[lastDate.strftime("%b")] = timer
                            for i in range(0,24):
                                timer[i] = 0             
                    
                    hourTotal += float(row.get('Consumption (kWh)', 0))      
                    preHour = date.hour
                    lastMonth = date.month
                    lastDate = date

                elif testDate == endDate and beacon == 0:
                
                    timer[preHour] = float(timer[preHour]) + hourTotal
                    print(timer)
                    hourTotal = 0
                    for i in range(0,24):
                        timer[i] = timer[i] / lastDate.day
                        
                    if lastDate.strftime("%b") in df:
                        current = df[lastDate.strftime("%b")]
                        current = current.to_numpy()
                        for i in range(0, len(current)):
                            timer[i] = (timer[i] + current[i])/2
                        print("KARAK\n",current)
                    df[lastDate.strftime("%b")] = timer 
                    beacon +=1                       





            print(df)


            fig, ax = plt.subplots()
            fig.set_figheight(8)
            fig.set_figwidth(16)

            
            ax.plot(df, label = df.columns)            

            leg = ax.legend()

            ax.set(xlabel='Hours', ylabel='Consumption (kW)', title='Average Hourly Consumption by Month')
            ax.grid()
            
            
            buf = BytesIO()
            fig.savefig(buf, format="png")

            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            file.close()
            return f"<img src='data:hoursByMonth/png;base64,{data}'/>", render_template("hoursByMonth.html")

    @app.route('/aggs')
    def monthlyAggs():
        
        csv.register_dialect('octopus', delimiter=',', skipinitialspace=True)

        with open('consumption.csv', 'r') as file:
            CSreader = csv.DictReader(file, delimiter = ',', skipinitialspace=True)        
        
        
            monthAggregates = []
            monthNumbers = []
            monthTotal = 0
            lastMonth = 1
            daysInMonth = 0
            
            for row in CSreader:
                date = datetime.datetime.fromisoformat(row.get('Start',0))

                if date.month != lastMonth:
                    monthTotalkw = monthTotal * daysInMonth * 24
                    monthAggregates.append(round(monthTotalkw, 3))
                    monthNumbers.append(monthDate.strftime("%m/%y"))
                    monthTotal = 0


                monthTotal += float(row.get('Consumption (kWh)', 0))      
                lastMonth = date.month
                daysInMonth = date.day
                monthDate = date
                
            
            monthTotalkw = monthTotal * daysInMonth * 24
            monthAggregates.append(round(monthTotalkw,3))
            monthNumbers.append(monthDate.strftime("%m/%y"))


            dataADDED = {'Months': monthNumbers,'Consumed': monthAggregates}
            df = pd.DataFrame(data=dataADDED)
            print(df)


            plt.figure(figsize=(24,8))
            plt.bar(df['Months'],df['Consumed'])

            def rounder(num, dp):
                multi = 10 ** dp
                return math.ceil(num * multi) / multi
            monthAggregates.sort(reverse=True)
            top = rounder(monthAggregates[0],-5)
            


            fig, ax = plt.subplots()
            fig.set_figheight(8)
            fig.set_figwidth(16)


            axes = plt.gca()
            axes.set_ylim([0,top])

            
            ax.bar(df['Months'], df['Consumed'])            


            ax.set(xlabel='Months', ylabel='Consumption (kW)', title="Aggregate Monthly Energy Consumption")
            
            
            
            buf = BytesIO()
            fig.savefig(buf, format="png")

            data = base64.b64encode(buf.getbuffer()).decode("ascii")

            file.close()            
            return f"<img src='data:hoursByMonth/png;base64,{data}'/>", render_template("aggs.html")







    



#TO DO
#REWORK WAYS GRAPHS ARE CODED
#PUT ALL ON ONE PAGE




    if __name__ == '__main__':
        app.run(debug = True)








