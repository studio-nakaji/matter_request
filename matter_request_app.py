import streamlit as st
import datetime as date
import calendar as cal
import time
import jpholiday

def check_holiday(day):
    if day.weekday() >= 5 or jpholiday.is_holiday(day):
        return 0
    else:
        return 1

def daterange(_start, _end):
    for n in range((_end - _start).days):
        yield _start + date.timedelta(n)

def get_days_money(start_day, end_day):
    start_month = start_day.month
    end_manth = end_day.month
    month = end_manth-start_month
    first_day = start_day.replace(day=1)
    last_day = end_day.replace(day=cal.monthrange(end_day.year, end_day.month)[1])
    #スタート日が月初から5日以内かつ、エンド日が月末から5日以内なら
    if first_day+date.timedelta(days=5)>start_day and last_day-date.timedelta(days=5)<end_day:
        return month, 20
    if month == 0:
        first_day = start_day.replace(day=1)
        last_day = end_day.replace(day=cal.monthrange(end_day.year, end_day.month)[1])
        remaining_days = 0
        for i in daterange(first_day, last_day):
            remaining_days += check_holiday(i)
        remaining_days += check_holiday(last_day)
        return month, remaining_days
    else:
        #スタートの月のスタート日〜月末までの平日を計算
        last_day = start_day.replace(day=cal.monthrange(start_day.year, start_day.month)[1])
        remaining_days = 0
        for i in daterange(start_day, last_day):
            remaining_days += check_holiday(i)
        remaining_days += check_holiday(last_day)
        #エンド月の月初〜エンド日までの平日を計算
        first_day = end_day.replace(day=1)
        for i in daterange(first_day, end_day):
            remaining_days += check_holiday(i)
        remaining_days += check_holiday(end_day)
        month = month-1
        return month, remaining_days
        

today = date.datetime.today()
end_day = today + date.timedelta(days=60)
"""
## Nスタへの発注依頼
"""
""
"発注のご相談ありがとうございます！"
"下記に詳細の入力をお願いします。"
""
st.text_input(label="作品タイトル", help="作品タイトルを入力して下さい")
summary_list_all = ["A:美術監督の依頼","B:コンセプトアート作業", "C:美術設定作業", "D:3Dモデル制作作業", "E:背景作業"]
genre_list = ["","TVシリーズ", "劇場", "版権", "その他"]
genre = st.selectbox(label="種類を選択",options=genre_list, help="Youtube用背景・漫画用背景などは[その他]を選択して下さい")
if genre == genre_list[1] or genre == genre_list[2]:
    summary_list = summary_list_all
elif genre == genre_list[3]:
    summary_list = ["D:3Dモデル制作作業", "E:背景作業"]
else:
    summary_list = ["B:コンセプトアート作業", "D:3Dモデル制作作業", "E:背景作業"]
if genre != "":
    summary = st.multiselect(label="依頼項目の選択",options=summary_list)
    #美監作業
    if summary_list_all[0] in summary:
        """
        ### A: 美監作業
        """
        if genre == genre_list[2]:              #劇場作品なら
            base_restraint_money = 450000
        elif genre == genre_list[1]:            #TVシリーズなら
            base_restraint_money = 350000
        else:                                   #TVシリーズ・劇場以外
            base_restraint_money = 400000
        left_column,right_column = st.columns(2)
        manager_start_day = left_column.date_input("A 開始日",min_value=today,value=today)
        manager_end_day = right_column.date_input("A 終了想定日",min_value=today,value=end_day)
        manager_monay = left_column.number_input("A 月額拘束料金(円)/1人",value=base_restraint_money, step=10000)
        manager_human = left_column.number_input("E 人数",value=1, step=1)
        sub_manager_check = left_column.checkbox("美監補佐",False)
        #日割り計算の日数を取得
        manager_month_range, work_renge = get_days_money(manager_start_day,manager_end_day)
        left_column.write(f"小計:¥{int(manager_month_range*manager_human*manager_monay+work_renge/20*manager_human*manager_monay)}")
    #コンセプトアート作業
    if summary_list_all[1] in summary:
        """
        ### B: コンセプトアート作業
        """
        left_column,right_column = st.columns(2)
        concept_start_day = left_column.date_input("B 開始日",min_value=today,value=today)
        concept_end_day = right_column.date_input("B 終了想定日",min_value=today,value=end_day)
        concept_work_type_list = ["拘束", "枚数単価"]
        concept_work_type = left_column.radio("B 料金形態",options=concept_work_type_list)
        #日割り計算の日数を取得
        month_range, work_renge = get_days_money(concept_start_day,concept_end_day)
        left_column,right_column = st.columns(2)
        if concept_work_type == concept_work_type_list[0]:
            concept_monay = left_column.number_input("B 月額拘束料金(円)/1人",value=400000, step=1000)
            concept_human = left_column.number_input("E 人数",value=1, step=1)
            left_column.write(f"小計:¥{int(month_range*concept_human*concept_monay+work_renge/20*concept_human*concept_monay)}")
        else:
            concept_num = left_column.number_input("B 枚数",value=5)
            concept_monay = right_column.number_input("B 単価(円)",value=40000, step=5000)
    #設定作業
    if summary_list_all[2] in summary:
        """
        ### C: 設定作業
        """
        left_column,right_column = st.columns(2)
        settei_start_day = left_column.date_input("C 開始日",min_value=today,value=today)
        settei_end_day = right_column.date_input("C 終了想定日",min_value=today,value=end_day)
        settei_work_type_list = ["拘束", "シーン単価"]
        settei_work_type = left_column.radio("C 料金形態",options=settei_work_type_list)
        #日割り計算の日数を取得
        settei_month_range, work_renge = get_days_money(settei_start_day,settei_end_day)
        left_column,right_column = st.columns(2)
        if settei_work_type == settei_work_type_list[0]:    #拘束の場合
            settei_monay = left_column.number_input("C 月額拘束料金(円)/1人",value=300000, step=5000)
            settei_human = left_column.number_input("E 人数",value=1, step=1)
            left_column.write(f"小計:¥{int(month_range*settei_human*settei_monay+work_renge/20*settei_human*settei_monay)}")
        else:                                               #単価の場合
            settei_num = left_column.number_input("C 数量(シーン数)",value=5)
            settei_monay = right_column.number_input("C 単価(円)",value=20000, step=1000)

    #3Dモデル作業
    if summary_list_all[3] in summary:
        """
        ### D: 3Dモデル作業
        """
        if genre == genre_list[2]:              #劇場作品なら
            base_restraint_money = 450000
            base_work_money = 250000
            work_money_step = 10000
        elif genre == genre_list[1]:            #TVシリーズなら
            base_restraint_money = 400000
            base_work_money = 200000
            work_money_step = 10000
        else:                                   #TVシリーズ・劇場以外
            base_restraint_money = 450000
            base_work_money = 250000
            work_money_step = 10000
        left_column,right_column = st.columns(2)
        model_start_day = left_column.date_input("D 開始日",min_value=today,value=today)
        model_end_day = right_column.date_input("D 終了想定日",min_value=today,value=end_day)
        model_work_type_list = ["拘束", "モデル単価"]
        model_work_type = left_column.radio("D 料金形態",options=model_work_type_list)
        #日割り計算の日数を取得
        model_month_range, model_work_renge = get_days_money(model_start_day,model_end_day)
        left_column,right_column = st.columns(2)
        if model_work_type == model_work_type_list[0]:
            model_monay = left_column.number_input("D 月額拘束料金(円)/1人",value=base_restraint_money, step=10000)
            model_human = left_column.number_input("E 人数",value=1, step=1)
            left_column.write(f"小計:¥{int(model_month_range*model_human*model_monay+model_work_renge/20*model_human*model_monay)}")
        else:
            model_num = left_column.number_input("D モデル数",value=5)
            model_monay = right_column.number_input("D 単価(円)",value=base_work_money, step=work_money_step)
    #背景作業
    if summary_list_all[4] in summary:
        """
        ### E: 背景作業
        """
        left_column,right_column = st.columns(2)
        if genre == genre_list[2]:              #劇場作品なら
            base_restraint_money = 350000
            base_work_money = 20000
            work_money_step = 1000
        elif genre == genre_list[1]:            #TVシリーズなら
            base_restraint_money = 300000
            base_work_money = 10000
            work_money_step = 100
            #話数指定の有無
            num_range_check = left_column.checkbox("話数指定",False)
            if num_range_check == False:
                num_range = right_column.slider("本数",min_value=1, max_value=24, value=(1,5))
                num_range = max(num_range)-min(num_range)+1
            else:
                num_range = len(right_column.multiselect("話数(複数選択可)",options=range(1,25)))
                left_column.write(f"{len(num_range)}話")
        else:                                   #TVシリーズ・劇場以外
            base_restraint_money = 400000
            base_work_money = 15000
            work_money_step = 100
            
        left_column,right_column = st.columns(2)
        work_start_day = left_column.date_input("E 開始日", min_value=today,value=today)
        work_end_days = right_column.date_input("E 終了想定日(納品日)", min_value=today,value=end_day)
        #日割り計算の日数を取得
        month_range, work_renge = get_days_money(work_start_day,work_end_days)
        
        work_type_list = ["拘束", "カット単価"]
        work_type = left_column.radio("E 料金形態",options=work_type_list)
        left_column,right_column = st.columns(2)
        if work_type == work_type_list[0]:      #拘束契約の場合
            work_monay = left_column.number_input("E 月額拘束料金(円)/1人",value=base_restraint_money, step=5000)
            work_human = left_column.number_input("E 人数",value=1, step=1)
            left_column.write(f"小計:¥{int(month_range*work_human*work_monay+work_renge/20*work_human*work_monay)}")
        else:
            cut_num = left_column.number_input("E カット数/1話",value=10)
            work_monay = right_column.number_input("E 単価(円)",value=base_work_money, step=work_money_step)
            if genre != genre_list[4]:
                if num_range_check == True:
                    if len(num_range)>1:
                        left_column.write(f"小計:¥{int(num_range*cut_num*work_monay)}")
                else:
                    left_column.write(f"小計:¥{num_range*cut_num*work_monay:,}円")
    # days = st.slider("日数",7,180)
    

if genre != "" and len(summary)>0:
    st.button("上記の内容で依頼する")