"""
:: Python for Humanities 期末專案 ::
:: Period Helper/生理週期小幫手 ::
:: Ou Yang Ju Hsin ::

    專案簡介：w
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
import hashlib
#from Crypto.Cipher import AES
import base64

def read():
    filename = 'PeriodHelper_doc.csv'
    df_encode = pd.read_csv(filename, header = 0, delimiter = ",")
    index = range(0, len(df_encode))
    df = pd.DataFrame(index=index, columns=columns)
    for i in index:
        for c in columns:
            ff = base64.b64decode(df_encode.loc[i, c])
            frag = ff.decode()
            df.loc[i, c] = frag
    return df




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
    if len(period) == 1:
        return('standard', 0, 0, 0, 0)
    else:
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

def pred_prog(calc_res1, calc_res2, df, calc_res4):
    if calc_res1 == 'standard':
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = 28)
        n_per_end_date = n_per_start_date + timedelta(days = 5)
        n_lut_start_date = n_per_start_date + timedelta(days = -18)
        n_lut_end_date = n_per_start_date + timedelta(days = -10)
        return (n_per_start_date, n_per_end_date, n_lut_start_date, n_lut_end_date)
    elif calc_res1 == 'var_var': ## 都不準 ##R應該是說上次end到下次start的天數
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'cycle']))
        n_per_end_date = n_per_start_date + timedelta(days = int(df.loc[index, 'period']))
        if 8 < (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days < 18:
            n_lut_start_date =  datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'period'])/2 - 4)
            n_lut_end_date = n_lut_start_date + timedelta(days = 8)
        elif (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days <= 8:
            n_lut_start_date = datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d").date() + timedelta(days = 1)
            n_lut_end_date = n_per_start_date + timedelta(days = -1)
        else:
            n_lut_start_date = n_per_start_date + timedelta(days = -18)
            n_lut_end_date = n_per_start_date + timedelta(days = -10)
        print(datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d"))
        print(datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d"))
        print((datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days)
        print(n_lut_start_date)
        print(n_lut_end_date)
        return (n_per_start_date, n_per_end_date, n_lut_start_date, n_lut_end_date)
    elif calc_res1 == 'var_sta': ##cycle準
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(calc_res4))
        n_per_end_date = n_per_start_date + timedelta(days = int(df.loc[index, 'period']))
        if 8 < (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days < 18:
            n_lut_start_date =  datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'period'])/2 - 4)
            n_lut_end_date = n_lut_start_date + timedelta(days = 8)
        elif (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days <= 8:
            n_lut_start_date = datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d").date() + timedelta(days = 1)
            n_lut_end_date = n_per_start_date + timedelta(days = -1)
        else:
            n_lut_start_date = n_per_start_date + timedelta(days = -18)
            n_lut_end_date = n_per_start_date + timedelta(days = -10)
        return (n_per_start_date, n_per_end_date, n_lut_start_date, n_lut_end_date)
    elif calc_res1 == 'sta_var': ##per準
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'cycle']))
        n_per_end_date = n_per_start_date + timedelta(days = calc_res2)
        if 8 < (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days < 18:
            n_lut_start_date =  datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'period'])/2 - 4)
            n_lut_end_date = n_lut_start_date + timedelta(days = 8)
        elif (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days <= 8:
            n_lut_start_date = datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d").date() + timedelta(days = 1)
            n_lut_end_date = n_per_start_date + timedelta(days = -1)
        else:
            n_lut_start_date = n_per_start_date + timedelta(days = -18)
            n_lut_end_date = n_per_start_date + timedelta(days = -10)
        return (n_per_start_date, n_per_end_date, n_lut_start_date, n_lut_end_date)
    else: ## 都準
        index = len(df)-1
        n_per_start_date = datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = calc_res4)
        n_per_end_date = n_per_start_date + timedelta(days = calc_res2)
        if 8 < (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days < 18:
            n_lut_start_date =  datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date() + timedelta(days = int(df.loc[index, 'period'])/2 - 4)
            n_lut_end_date = n_lut_start_date + timedelta(days = 8)
        elif (datetime.datetime.strptime(str(n_per_start_date), "%Y-%m-%d") - datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).days <= 8:
            n_lut_start_date = datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d").date() + timedelta(days = 1)
            n_lut_end_date = n_per_start_date + timedelta(days = -1)
        else:
            n_lut_start_date = n_per_start_date + timedelta(days = -18)
            n_lut_end_date = n_per_start_date + timedelta(days = -10)
        return (n_per_start_date, n_per_end_date, n_lut_start_date, n_lut_end_date)
    


## 今日的小提醒
def reminder():
    while True:
        df = read()
        period_data = []
        cycle_data = []
        for i in range(0, len(df)):
            if (datetime.date.today() - datetime.datetime.strptime(df['end_date'][i], "%Y/%m/%d").date()).days <90:
                period_data.append(int(df['period'][i]))
        for i in range(1, len(df)):
                if (datetime.date.today() - datetime.datetime.strptime(df['end_date'][i], "%Y/%m/%d").date()).days <90:
                    cycle_data.append(int(df['cycle'][i]))
        if len(period_data) == 0:
            print(len(['1', ]))
            print(period_data)
            print('近三個月無資料，無法生成小提醒！')
            print('即將自動回到功能列...')
            time.sleep(1)
            break
        else:
            calc_res = calc(period_data, cycle_data)
            pred_prog_res = pred_prog(calc_res[0], calc_res[2], df, calc_res[4])
            td = datetime.date.today()
            index = len(df)-1
            print('==========今日的小提醒===========')
            if pred_prog_res[0] < td < pred_prog_res[1]:
                print('今天可能是行經期，辛苦囉！記得帶衛生棉、多休息、多吃綠色蔬菜。\n'+
                '如果行經期沒有如期到來，要多休息、注意保暖、少吃生冷食物，多運動也會有幫助！')
            elif pred_prog_res[2] < td < pred_prog_res[3]:
                print('今天在排卵期，想造人可以多加把勁，若還沒有規劃則宜多加注意。')
            elif 0 < (pred_prog_res[0] - td).days < 7:
                print('行經期快到囉！可以開始注意包包裡的衛生用品夠不夠，\n' + 
                '可能會比較疲累，行程別排太滿，最好不要吃生冷、刺激的食物。')
            elif 0 < (td - datetime.datetime.strptime(df.loc[index, 'start_date'], "%Y/%m/%d").date()).days < 7:
                print('行經期差不多離開了，現在是最佳進補時機喔。')
            else:
                print('子宮默默運作中，請善待它，多喝溫開水。')
            print('===知道了，按enter回到主功能列===')
            leavema = input('>> ')
            if input == '':
                break
            else:
                break


## 生理週期預測
def pred():
    while True:
        df = read()
        period_data = []
        cycle_data = []
        for i in range(0, len(df)):
            if (datetime.date.today() - datetime.datetime.strptime(df['end_date'][i], "%Y/%m/%d").date()).days <90:
                period_data.append(int(df['period'][i]))
        for i in range(1, len(df)):
            if (datetime.date.today() - datetime.datetime.strptime(df['end_date'][i], "%Y/%m/%d").date()).days <90:
                cycle_data.append(int(df['cycle'][i]))
        if len(period_data) == 0:
            print('近三個月無資料，無法生成預測！')
            print('即將自動回到功能列...')
            time.sleep(1)
            break
        else:
            calc_res = calc(period_data, cycle_data)
            pred_prog_res =pred_prog(calc_res[0], calc_res[2], df, calc_res[4])
            print("""預測結果:
            排卵期：{}～{}
            行經期：{}～{}""".format(
                            pred_prog_res[2], pred_prog_res[3], pred_prog_res[0], pred_prog_res[1]))
            print('*此預測結果僅供參考。')
            if calc_res[1] != 'sta_sta':
                print('*生理週期、行經期天數不規律及資料量不足都會影響預測準確性。')
            print('===預測完畢，按enter回到主功能列===')
            leavema = input('>> ')
            if input == '':
                break
            else:
                break



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
            try:
                datetime.datetime.strptime(start_date, "%Y/%m/%d")
                pass
            except:
                print('輸入有誤！請重新輸入！')
                continue
            while not check_date(start_date):
                start_date = input('')
            get_data.append(start_date)
            end_date = input(' 輸入結束日期：')
            try:
                datetime.datetime.strptime(start_date, "%Y/%m/%d")
                pass
            except:
                print('輸入有誤！請重新輸入！')
                continue
            if end_date == '':
                break
            elif datetime.datetime.strptime(start_date, "%Y/%m/%d") > datetime.datetime.strptime(end_date, "%Y/%m/%d"):
                print('開始日期不可在結束日期之後，請重新輸入！')
                continue
            else:
                while not check_date(end_date):
                    end_date = input('')
                get_data.append(end_date)
                perday = str((datetime.datetime.strptime(end_date, "%Y/%m/%d").date() - datetime.datetime.strptime(start_date, "%Y/%m/%d").date()).days + 1)
                get_data.append(perday)
                get_data.append('0')
                df = read()
                df.loc[len(df)] = get_data
                df_sort = df.sort_values(by=['start_date']).copy()
                for i in range(0, len(df_sort)):
                    for c in columns:
                        df_sort.loc[i, c] = str(base64.b64encode(str(df_sort.loc[i, c]).encode()), encoding = "utf-8")      
                df_sort.to_csv(filename, index=False)

                df = read()
                frag = True
                for i in range(1, len(df)):
                    if datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date() <= datetime.datetime.strptime(df['end_date'][i-1], "%Y/%m/%d").date():
                        print('與先前資料重疊，請重新輸入！')
                        frag = False
                        df_dropped = df.drop(df.index[i])
                        df = df_dropped
                        break
                    get_cycle = (datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date() - datetime.datetime.strptime(df['start_date'][i-1], "%Y/%m/%d").date()).days
                    df.loc[i,'cycle'] = get_cycle
                for i in range(0, len(df)):
                    for c in columns:
                        df.loc[i, c] = str(base64.b64encode(str(df.loc[i, c]).encode()), encoding = "utf-8")      
                df.to_csv(filename, index=False)
                if frag:
                    print('==紀錄完成，即將自動回到功能列。==')
                    time.sleep(1)
                    break


 
 
## 生理週期規律程度分析
def analy():
    df = read()
    period_data = []
    cycle_data = []
    index = len(df)-1
    print("""====生理週期規律程度分析====
選擇分析範圍：
1. 全部範圍
2. 近三個月內
或按enter回到主功能列""")
    while True:
        get_ran = input('請輸入：')
        if get_ran == "":
            break
        elif get_ran == "1":
            for i in range(0, len(df)):
                period_data.append(int(df['period'][i]))
            for i in range(1, len(df)):
                cycle_data.append(int(df['cycle'][i]))
        elif get_ran == "2":
            for i in range(0, len(df)):
                if (datetime.date.today() - datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date()).days <90:
                    period_data.append(int(df['period'][i]))
            for i in range(1, len(df)):
                if (datetime.date.today() - datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date()).days <90:
                    cycle_data.append(int(df['cycle'][i]))
        else:
            print('輸入有誤喔！')
            continue
        calc_res = calc(period_data, cycle_data)
        ## 規律程度判斷
        if calc_res[0] == 'sta_sta':
            reg = '生理週期與行經期天數都規律。'
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
                elif calc_res[3] <21:
                    dur = '生理週期天數和行經期天數都遠低於普遍值，建議諮詢婦產科。'
                else:
                    dur = '生理週期天數遠低於普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
            else:
                if calc_res[3] >35:
                    dur = '生理週期天數遠超過普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
                elif calc_res[3] <21:
                    dur = '生理週期天數遠低於普遍值，行經期天數在普遍值內，建議諮詢婦產科。'
                else:
                    dur = '生理週期天數和行經期天數都在普遍值內。'
            print(">> 生理週期規律性分析結果：{}\n>> 生理週期長度分析結果：{}（生理週期平均長度{}天，行經期平均長度{}天。）".format(
                    reg, dur, calc_res[2], calc_res[4]))
        else:
            if calc_res[0] == 'var_var':
                reg = '生理週期與行經期天數都不規律喔！建議諮詢婦產科。'
            elif calc_res[0] == 'var_sta':
                reg = '生理週期規律性分析結果：生理週期規律，行經期天數不規律，建議諮詢婦產科。'
            elif calc_res[0] == 'sta_var':
                reg = '生理週期規律性分析結果：行經期天數規律，生理週期不規律，建議諮詢婦產科。'
## 時間長度判斷
            if int(df.loc[index, 'period']) > 8:
                if 35 < (datetime.date.today() - (datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).date()).days or int(df.loc[index, 'cycle']) >35:
                    dur = '最近一次生理週期天數及行經期天數皆遠超過普遍值，建議多加注意或諮詢婦產科。'
                elif int(df.loc[index, 'cycle']) <14:
                    dur = '最近一次生理週期天數低於普遍值，行經期天數遠超過普遍值，建議多加注意或諮詢婦產科。'
                else:
                    dur = '最近一次生理週期天數在普遍值內，行經期天數遠超過普遍值，建議多加注意或諮詢婦產科。'
            elif int(df.loc[index, 'period']) < 2:
                if 35 < (datetime.date.today() - (datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).date()).days or int(df.loc[index, 'cycle']) >35:
                    dur = '最近一次生理週期天數遠超過普遍值，行經期天數遠低於普遍值，建議多加注意或諮詢婦產科。'
                elif int(df.loc[index, 'cycle']) <14:
                    dur = '最近一次生理週期天數和行經期天數皆遠低於普遍值，建議多加注意或諮詢婦產科。'
                else:
                    dur = '最近一次生理週期天數遠低於普遍值，行經期天數在普遍值內，建議多加注意或諮詢婦產科。'
            else:
                if 35 < (datetime.date.today() - (datetime.datetime.strptime(df.loc[index, 'end_date'], "%Y/%m/%d")).date()).days or int(df.loc[index, 'cycle']) >35:
                    dur = '最近一次生理週期天數遠超過普遍值，行經期天數在普遍值內，建議多加注意或諮詢婦產科。'
                elif int(df.loc[index, 'cycle']) <14:
                    dur = '最近一次生理週期天數遠低於普遍值，行經期天數在普遍值內，建議多加注意或諮詢婦產科。'
                else:
                    dur = '最近一次生理週期天數和行經期天數都在普遍值內。'
            print(">> 生理週期規律性分析結果：{}\n>> 生理週期長度分析結果：{}".format(
                    reg, dur))          
        print('===分析完畢，按enter回到主功能列===')
        leavema = input('>> ')
        if input == '':
            break
        else:
            break




## 生理週期歷史資料
def history():
    df = read()
    while True:
        counter = 1
        print('============歷史資料============')
        for i in range(0, len(df)):
            print("{}:{}-{}, 行經期{}天, 生理週期{}天".format(
                counter, df['start_date'][i], df['end_date'][i], df['period'][i], df['cycle'][i]))
            counter += 1
        print("===資料結束，按enter回到主功能列===")
        leavema = input('>> ')
        if input == '':
            break
        else:
            break
        break

## 刪除資料
def delete():
    df = read()
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
        delete_index = input('輸入欲刪除的資料代碼，或按enter回到主功能列：')
        ## 輸入i，是要取資料中index的第i-1筆
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
                    get_cycle = (datetime.datetime.strptime(df['start_date'][i], "%Y/%m/%d").date() - datetime.datetime.strptime(df['start_date'][i-2], "%Y/%m/%d").date()).days
                    df.loc[i,'cycle'] = get_cycle
                df_new = df.drop(df.index[i-1])
                df_new = df_new.reset_index(drop=True)
                for i in range(0, len(df_new)):
                    for c in columns:
                        df_new.loc[i, c] = str(base64.b64encode(str(df_new.loc[i, c]).encode()), encoding = "utf-8")  
                df_new.to_csv(filename, index=False)
                df = read()
                print('資料已更新！')
                print('===========更新後資料============')
                counter = 1
                for i in range(0, len(df)):
                    print("{}:{}-{}, 行經期{}天, 生理週期{}天".format(
                        counter, df['start_date'][i], df['end_date'][i], df['period'][i], df['cycle'][i]))
                    counter += 1
                print("===資料結束，按enter回到主功能列===")
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
                elif hashlib.md5(getpin.encode('utf-8')).hexdigest() != pin[0]:
                    print('密碼錯誤，請重新輸入！')
                    continue
                else:
                    while True:
                        makepin = input('重新設定，請設定四位數字密碼，或按enter離開\n密碼：')
                        if hashlib.md5(makepin.encode('utf-8')).hexdigest() == pin[0]:
                            print('新密碼不可等同於舊密碼！')
                            continue
                        if makepin.isdigit() == True and len(makepin) == 4:
                            with open('PeriodHelper_pin.csv', 'w') as csvfile:
                                password = makepin
                                writer = csv.writer(csvfile)
                                writer.writerow([hashlib.md5(makepin.encode('utf-8')).hexdigest()])
                                print('==更改成功！即將自動回到功能列。==')
                                time.sleep(1)
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
            password = makepin
            with open('PeriodHelper_pin.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([hashlib.md5(makepin.encode('utf-8')).hexdigest()])
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
                elif hashlib.md5(getpin.encode('utf-8')).hexdigest() != pin[0]:
                    print('密碼錯誤，請重新輸入！')
                    continue
                else:
                    password = getpin
                    return
            break

password = ''
filename = 'PeriodHelper_doc.csv'
columns = ['start_date', 'end_date', 'period', 'cycle']
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

