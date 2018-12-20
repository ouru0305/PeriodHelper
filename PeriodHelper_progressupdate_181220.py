"""
:: Python for Humanities 期末專案 ::
:: Period Helper/生理週期小幫手 ::
:: Ou Yang Ju Hsin ::

    專案簡介：
        PeriodHelper幫助使用者更從容地掌握、面對生理週期。
        除了幫助使用者紀錄生理週期，也利用紀錄資料替使用者
        分析判斷生理週期是否規律、正常，預測下一次生理週期
        ，並被動提供每日的小提醒。

"""



## import
import csv
import re
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import time

def calc(period, cycle):
    ## 行經期標準差
    period_std = np.std(period)
    ## 行經期平均數
    period_avg = sum(period)/len(period)
    peravg_pri = int(round(period_avg))
    ## 生理週期標準差
    cycle_std = np.std(cycle)
    ## 生理期平均數
    cycle_avg = sum(cycle)/len(cycle)
    cycavg_pri = int(round(cycle_avg))
    if period_std > 1.5:
        if cycle_std >5:
            return('var_var', period_avg, peravg_pri, cycle_avg, cycavg_pri)
        else:
            return('var_sta', period_avg, peravg_pri, cycle_avg, cycavg_pri)
    else:
        if cycle_std >5:
            return('sta_var', period_avg, peravg_pri, cycle_avg, cycavg_pri)
        else:
            return('sta_sta', period_avg, peravg_pri, cycle_avg, cycavg_pri)



## 今日的小提醒
def reminder():
    print('reminder is not implemented yet')
    pass  # function to be implemented

## 生理週期預測
def pred():
    filename = 'PeriodHelper_doc.csv'
    df = pd.read_csv(filename, header = 0, delimiter = ",")
    period_data = []
    cycle_data = []
    for i in range(1, len(df)):
                if (datetime.date.today() - datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date()).days <90:
                    period_data.append(df['period'][i])
                    cycle_data.append(df['cycle'][i])
    calc_res = calc(period_data, cycle_data)
    if calc_res[0] == 'var_var': ## 都不準
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = df.loc[index, 'cycle'])
        n_per_end_date = n_per_start_date + timedelta(days = df.loc[index, 'period'])
        n_lut_start_date = n_per_start_date + timedelta(days = -18)
        n_lut_start_end = n_per_start_date + timedelta(days = -10)
    elif calc_res[0] == 'var_sta': ##cycle準
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = calc_res[4])
        n_per_end_date = n_per_start_date + timedelta(days = df.loc[index, 'period'])
        n_lut_start_date = n_per_start_date + timedelta(days = -18)
        n_lut_start_end = n_per_start_date + timedelta(days = -10)
    elif calc_res[0] == 'sta_var': ##per準
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = df.loc[index, 'cycle'])
        n_per_end_date = n_per_start_date + timedelta(days = df.loc[index, calc_res[2])
        n_lut_start_date = n_per_start_date + timedelta(days = -18)
        n_lut_start_end = n_per_start_date + timedelta(days = -10)
    else:
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = calc_res[4])
        n_per_end_date = n_per_start_date + timedelta(days = calc_res[2])
        n_lut_start_date = n_per_start_date + timedelta(days = -18)
        n_lut_start_end = n_per_start_date + timedelta(days = -10)
    print("""預測結果:
    排卵期：{}~{}
    行經期{}~{}""".format(
                    n_lut_start_date, n_lut_start_end, n_per_start_date, n_per_end_date))



##  check date
def check_date(inputdate):
    try:
        checking = datetime.datetime.strptime(inputdate, "%Y/%m/%d")
        return True
    except ValueError:
        print('輸入有誤！再輸入一次：')
        return False




## 紀錄行經期日期
def doc():
    print('  [紀錄行經期日期]\n（格式：公元年份/月份/日期\n範例：2018/01/01）\n提醒:按enter回到主功能列')
    while True:
        get_data = []
        start_date = input(' 輸入開始日期：')
        if start_date == '':
            break
        else:
            while not check_date(start_date):
                start_date = input('')
            get_data.append(start_date)
            end_date = input(' 輸入結束日期：')
            if end_date == '':
                break
            elif datetime.datetime.strptime(start_date, "%Y/%m/%d") > datetime.datetime.strptime(end_date, "%Y/%m/%d"):
                print('輸入有誤！請重新輸入！')
                continue
            else:
                while not check_date(end_date):
                    end_date = input('')
                get_data.append(end_date)
                get_data.append((datetime.datetime.strptime(end_date, "%Y/%m/%d").date() - datetime.datetime.strptime(start_date, "%Y/%m/%d").date()).days + 1)
                get_data.append('0')
                filename = 'PeriodHelper_doc.csv'
                df = pd.read_csv(filename, header = 0, delimiter = ",")
                #headers = list(df.columns.values)
                df.loc[len(df)] = get_data
                df_sort = df.sort_values(by=['start_date']).copy()
                df_sort.to_csv(filename, index=False)
                df = pd.read_csv(filename, header = 0, delimiter = ",")
            
                frag = True
                for i in range(1, len(df)):
                    if datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date() <= datetime.datetime.strptime(df['end_date'][i-1], "%Y/%m/%d").date():
                        print('輸入有誤！請重新輸入！')
                        frag = False
                        df = df.drop(df.index[i])
                        df.to_csv(filename, index=False)
                        break
                    get_cycle = (datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date() - datetime.datetime.strptime(df['start_date'][i-1], "%Y/%m/%d").date()).days
                    df.loc[i,'cycle'] = get_cycle
                    df.to_csv(filename, index=False)
                if frag:
                    print('紀錄完成，即將自動回到功能表。')
                    time.sleep(1)
                    break


 
 
## 生理週期規律程度分析
def analy():
    filename = 'PeriodHelper_doc.csv'
    df = pd.read_csv(filename, header = 0, delimiter = ",")
    period_data = []
    cycle_data = []
    print("""====生理週期規律程度分析====
選擇分析範圍：
1. 全部範圍
2. 近三個月內
或按enter回到上一頁""")
    while True:
        get_ran = input('請輸入：')
        if get_ran == "":
            break
        elif get_ran == "1":
            for i in range(1, len(df)):
                period_data.append(df['period'][i])
                cycle_data.append(df['cycle'][i])
        elif get_ran == "2":
            for i in range(1, len(df)):
                if (datetime.date.today() - datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date()).days <90:
                    period_data.append(df['period'][i])
                    cycle_data.append(df['cycle'][i])
        else:
            print('輸入有誤喔！')
            continue
        calc_res = calc(period_data, cycle_data)
        ## 規律程度判斷
        if calc_res[0] == 'var_var':
            reg = '生理週期與行經期天數都不規律喔！建議諮詢婦產科。'
        elif calc_res[0] == 'var_sta':
                reg = '生理週期規律，行經期天數不規律，建議諮詢婦產科。'
        elif calc_res[0] == 'sta_var':
                reg ='行經期天數規律，生理週期不規律，建議諮詢婦產科。'
        else:
                reg ='恭喜！生理週期與行經期天數都規律。'
        ## 時間長度判斷
        if calc_res[1] > 8:
            if calc_res[3] >35:
                dur = '生理週期天數與行經期天數遠超過普遍值，建議諮詢婦產科。'
            elif calc_res[3] <14:
                dur = '生理週期天數遠低於普遍值，行經期天數遠超過普遍值，建議諮詢婦產科。'
            else:
                dur = '生理週期天數在普遍值內，行經期天數遠超過普遍值，建議諮詢婦產科。'
        elif calc_res[1] < 2:
            if calc_res[3] >35:
                dur = '生理週期天數遠超過普遍值，行經期天數遠低於普遍值，建議諮詢婦產科。'
            elif calc_res[3] <14:
                dur = '生理週期天數和行經期天數都遠低於普遍值，建議諮詢婦產科。'
            else:
                dur = '生理週期天數遠低於普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
        else:
            if calc_res[3] >35:
                dur = '生理週期天數遠超過普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
            elif calc_res[3] <14:
                dur = '生理週期天數遠低於普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
            else:
                dur = '恭喜！生理週期天數和行經期天數都在普遍值內。'
        print(">> 生理週期規律性分析結果：{}\n>> 生理週期長度分析結果：{}（生理週期平均長度{}天，行經期平均長度{}天。）".format(
                    reg, dur, calc_res[2], calc_res[4]))
        print('===分析完畢，按enter回到主功能表===')
        leavema = input('>> ')
        if input == '':
            break
        else:
            break




## 生理週期歷史資料
def history():
    filename = 'PeriodHelper_doc.csv'
    df = pd.read_csv(filename, header = 0, delimiter = ",")
    while True:
        counter = 1
        print('============歷史資料============')
        for i in range(0, len(df)):
            print("{}:{}-{}, 行經期{}天, 生理週期{}天".format(
                counter, df['start_date'][i], df['end_date'][i], df['period'][i], df['cycle'][i]))
            counter += 1
        print("===資料結束，按enter回到上一頁===")
        leavema = input('>> ')
        if input == '':
            break
        else:
            break
        break

## 刪除資料
def delete():
    filename = 'PeriodHelper_doc.csv'
    df = pd.read_csv(filename, header = 0, delimiter = ",")
    while True:
        counter = 1
        print('========歷史資料========')
        for i in range(0, len(df)):
            print("{}:{}-{}, 行經期{}天, 生理週期{}天".format(
                counter, df['start_date'][i], df['end_date'][i], df['period'][i], df['cycle'][i]))
            counter += 1
        print("========資料結束========")
        break
    while True:
        delete_index = input('輸入欲刪除的資料代碼，或按enter回到上一頁：')
        if delete_index == '':
            break
        else:
            try:
                i = int(delete_index)
                pass
            except:
                print('輸入有誤喔！')
                continue
            if i > len(df):
                print('輸入有誤喔！')
                continue
            else:
                if i == len(df):
                    pass
                elif i == 1:
                    df.loc[1,'cycle'] = 0
                else:
                    get_cycle = (datetime.datetime.strptime(df['start_date'][i+1], "%Y/%m/%d").date() - datetime.datetime.strptime(df['start_date'][i-1], "%Y/%m/%d").date()).days
                    df.loc[i+1,'cycle'] = get_cycle
                df_new = df.drop(df.index[i-1])
                df_new.to_csv(filename, index=False)
                df = pd.read_csv(filename, header = 0, delimiter = ",")
                print('資料已更新！')
                print('===========更新後資料============')
                counter = 1
                for i in range(0, len(df)):
                    print("{}:{}-{}, 行經期{}天, 生理週期{}天".format(
                        counter, df['start_date'][i], df['end_date'][i], df['period'][i], df['cycle'][i]))
                    counter += 1
                print("===資料結束，按enter回到上一頁===")
                leavema = input('>> ')
                if input == '':
                    break
                else:
                    break
        break





## 更改密碼
def change_pin():
    with open('PeriodHelper_pin.csv','r') as csvfile:
        pins = csv.reader(csvfile)
        for pin in pins:
            while True:
                getpin = input('請輸入原密碼，或按enter離開：')
                if getpin == '':
                    break
                elif getpin != pin[0]:
                    print('密碼錯誤，請重新輸入！')
                    continue
                else:
                    while True:
                        makepin = input('重新設定，請設定四位數字密碼，或按enter離開\n密碼：')
                        if makepin.isdigit() == True and len(makepin) == 4:
                            with open('PeriodHelper_pin.csv', 'w') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([makepin])
                                print('更改成功！')
                                break
                        elif makepin == '':
                            break
                        else:
                            print('輸入有誤，請重新輸入！')
                break
            break




## get_order
def get_order():
    while True:
        order = input('選擇功能：')
        if order == "":
            exit()
        elif order == "1":
            reminder()
            break
        elif order == "2":
            pred()
            break
        elif order == "3":
            doc() 
            break
        elif order == "4":
            analy()
            break
        elif order == "5":
            history()
            break
        elif order == "6":
            delete()
            break
        elif order == "7":
            change_pin()
            break
        else:
            print('輸入有誤喔！')
        


## main
def main():
    while True:
        print("""===Period Helper===
按1進入 今日的小提醒
按2進入 生理週期預測
按3進入 紀錄行經期日期
按4進入 生理週期規律程度分析
按5進入 生理週期歷史資料
按6進入 刪除資料
按7進入 更改密碼
按enter 離開程式、登出""")
        get_order()


## 設定密碼
def make_pin():
    while True:
        makepin = input('第一次使用，請設定四位數字密碼，或按enter離開\n密碼：')
        if makepin.isdigit() == True and len(makepin) == 4:
            with open('PeriodHelper_pin.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([makepin])
                break
        elif makepin == '':
            exit()
        else:
            print('輸入有誤，請重新輸入！')


## 輸入密碼
def check_pin():
    with open('PeriodHelper_pin.csv','r') as csvfile:
        pins = csv.reader(csvfile)
        for pin in pins:
            while True:
                getpin = input('請輸入密碼，或按enter離開：')
                if getpin == '':
                    exit()
                elif getpin != pin[0]:
                    print('密碼錯誤，請重新輸入！')
                    continue
                else:
                    return
            break

## 設定及輸入密碼
with open('PeriodHelper_pin.csv','r') as csvfile:
    pins = csv.reader(csvfile)
    for pin in pins:
        if pin[0] == "default":
            make_pin()
        else:
            check_pin()
        break
main()

