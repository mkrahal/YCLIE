'''
############################################################################
#                                                                          #
#       YLIE - Yield to Maturity Linear Interpolation Engine              #
#       ------------------------------------------------------             #
#                                                                          #
#                                                                          #
#  MIT License                                                             #
#  Copyright 2017 MK Rahal                                                 #
#                                                                          #
#  Permission is hereby granted, free of charge, to any person             #
#  obtaining a copy of this software and associated documentation          #
#  files (the "Software"), to deal in the Software without                 #
#  restriction, including without limitation the rights to use,            #
#  copy, modify, merge, publish, distribute, sublicense, and/or            #
#  sell copies of the Software, and to permit persons to whom the          #
#  Software is furnished to do so, subject to the following conditions:    #
#                                                                          #
#  The above copyright notice and this permission notice shall be          #
#  included in all copies or substantial portions of the Software.         #
#                                                                          #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES         #
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT             #
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,            #
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,      #
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER           #
#  DEALINGS IN THE SOFTWARE.                                               #
#                                                                          #
############################################################################
'''

import datetime
import decimal

# Maturity subject to yield rate interpolation (in days)
# ex. 8 years => 8*365
ResMat = 8*365

# SAMPLE yield curve data
# Note: to obtain a yield curve based on residual maturities, 
# the issue date should be replaced with current date.
YieldCurveList = [
        {"IssueDateDay":13, "IssueDateMonth":9, "IssueDateYear":2016, "TMDay":13, "TMMonth":12, "TMYear":2018, "Yield":2.430},
        {"IssueDateDay":15, "IssueDateMonth":10, "IssueDateYear":2016, "TMDay":15, "TMMonth":10, "TMYear":2021, "Yield":2.877},
        {"IssueDateDay":20, "IssueDateMonth":11, "IssueDateYear":2016, "TMDay":20, "TMMonth":11, "TMYear":2026, "Yield":3.245},
                 ]


# Extract yield curve data from YieldCurveList and prepare lists for matrix insertion
def YieldCurveDataPoints(YieldCurveList):
    # ##YieldCurve Data##
    TMYearList = []
    TMMonthList = []
    TMDayList = []
    IssueDateYearList = []
    IssueDateMonthList = []
    IssueDateDayList = []
    YieldList = []

    for row in YieldCurveList:
        TMYearList.append(row["TMYear"])
        TMMonthList.append(row["TMMonth"])
        TMDayList.append(row["TMDay"])
        IssueDateYearList.append(row["IssueDateYear"])
        IssueDateMonthList.append(row["IssueDateMonth"])
        IssueDateDayList.append(row["IssueDateDay"])
        YieldList.append(decimal.Decimal(row["Yield"]))

    return TMYearList, TMMonthList, TMDayList, IssueDateYearList, IssueDateMonthList, IssueDateDayList, YieldList


# Generate data sets & populate the yield curve matrix
def YieldMatrix(TMYearList, TMMonthList, TMDayList, IssueDateYearList, IssueDateMonthList, IssueDateDayList, YieldList):
    YieldCurve = []
    MaxEntries = len(YieldList)
    index = 0
    while index < MaxEntries:  
        TerminalMaturity = datetime.date(TMYearList[index], TMMonthList[index], TMDayList[index])
        IssueDate = datetime.date(IssueDateYearList[index], IssueDateMonthList[index], IssueDateDayList[index])
        ResidualMaturity = TerminalMaturity - IssueDate
        YieldCurve.extend([[IssueDate, TerminalMaturity, ResidualMaturity.days, YieldList[index]]])
        index = index + 1
    return YieldCurve


# Locate interpolation data points in yield curve matrix
def Locate_Interp_Points(YieldCurve):
    LineIndex = 0
    for lines in YieldCurve:
        if ResMat > lines[2]:
            LineIndex = LineIndex + 1
        else:
            return LineIndex


# Interpolate yield (linear interpolation)
def interpolate_yield(YieldCurve, LowerLimit, UpperLimit):
    Y_M0 = YieldCurve[LowerLimit][3]
    Y_M1 = YieldCurve[UpperLimit][3]
    M_M0 = decimal.Decimal(ResMat)-decimal.Decimal(YieldCurve[LowerLimit][2])
    M1_M0 = decimal.Decimal(YieldCurve[UpperLimit][2]) - decimal.Decimal(YieldCurve[LowerLimit][2])
    Interp_Yield = Y_M0 + (Y_M1-Y_M0)*(M_M0/M1_M0)
    return Interp_Yield


# Main Switch Board
def main():
    
    TMYearList, TMMonthList, TMDayList, IssueDateYearList, IssueDateMonthList, IssueDateDayList, YieldList = YieldCurveDataPoints(YieldCurveList)

    YieldCurve = YieldMatrix(TMYearList, TMMonthList, TMDayList, IssueDateYearList, IssueDateMonthList, IssueDateDayList, YieldList)
    LineIndex = Locate_Interp_Points(YieldCurve)

    if LineIndex > 0:
        UpperLimit = LineIndex
        LowerLimit = LineIndex - 1
        Interp_Yield = interpolate_yield(YieldCurve, LowerLimit, UpperLimit)
    else:
        UpperLimit = LineIndex
        LowerLimit = LineIndex
        Interp_Yield = YieldCurve[LowerLimit][3]

    print "The Market Interpolated Yield Is: %6.3f%%" % (Interp_Yield)
    return 0

main()
