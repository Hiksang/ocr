## V12
import numpy as np
import pandas as pd
import panel as pn
import base64

import pandas as pd
import re
import shutil
from pandasai import Agent, SmartDataframe
import plotly.graph_objs as go
import plotly.io as pio


file_path = '2023_data.xlsx'
xls = pd.ExcelFile(file_path, engine='openpyxl')
sheets = {sheet_name: xls.parse(sheet_name, header=3) for sheet_name in xls.sheet_names}

def split_dataframe_by_sum(df, column_name):
    """
    주어진 DataFrame을 특정 열에서 '합계'를 기준으로 분할합니다.

    Parameters:
    df (pd.DataFrame): 분할할 DataFrame.
    column_name (str): '합계'를 검색할 열의 이름.

    Returns:
    list: '합계'를 포함한 각 부분으로 분할된 DataFrame의 리스트.
    """
    df.index = range(len(df))

    # 해당 열에서 '합계'가 있는 인덱스 찾기
    indices = df[df[column_name] == '합계'].index

    # DataFrame을 분할
    dataframes = []
    start_idx = 0

    for idx in indices:
        # '합계'를 포함하는 행까지 DataFrame 슬라이스
        dataframes.append(df.iloc[start_idx:idx+1])
        start_idx = idx + 1  # 다음 분할을 위해 시작 인덱스를 '합계' 다음 행으로 설정

    # 마지막 인덱스부터 DataFrame 끝까지 추가
    if start_idx < len(df):  # 마지막 '합계' 이후에도 데이터가 남아 있는 경우
        dataframes.append(df.iloc[start_idx:])

    return dataframes[0]

def split_dataframe_by_date(df, column_name):
    """
    주어진 DataFrame을 특정 열에서 '날짜'를 기준으로 분할합니다.

    Parameters:
    df (pd.DataFrame): 분할할 DataFrame.
    column_name (str): '날짜'를 검색할 열의 이름.

    Returns:
    list: '날짜'를 포함한 각 부분으로 분할된 DataFrame의 리스트.
    """
    df.index = range(len(df))
    df.columns = df.columns.str.replace('\n', '', regex=False)


    # 해당 열에서 '날짜'가 있는 인덱스 찾기
    indices = df[df[column_name] == '날짜'].index

    # DataFrame을 분할
    dataframes = []
    start_idx = 0

    for idx in indices+1:
        # '날짜'를 포함하는 행까지 DataFrame 슬라이스
        dataframes.append(df.iloc[start_idx:idx+1])
        start_idx = idx + 1  # 다음 분할을 위해 시작 인덱스를 '날짜' 다음 행으로 설정

    # 마지막 인덱스부터 DataFrame 끝까지 추가
    if start_idx < len(df):  # 마지막 '날짜' 이후에도 데이터가 남아 있는 경우
        dataframes.append(df.iloc[start_idx:])

    return dataframes[1]


# NaN 값을 이전 값으로 채우기
def fill_date(df):
    df['날짜'] = df['날짜'].fillna(method='ffill')

    return df


def convert_date_and_format(df, column, month):
    # 월을 나타내는 한글과 숫자를 매핑하는 딕셔너리
    month_dict = {'1월': '01', '2월': '02', '3월': '03', '4월': '04', '5월': '05', '6월': '06', 
                  '7월': '07', '8월': '08', '9월': '09', '10월': '10', '11월': '11', '12월': '12'}
    
    # 데이터 프레임의 복사본을 만듭니다.
    df_copy = df.copy()
    
    # 가정: df는 데이터 프레임, column은 변경하려는 열
    def convert_date(date, month):
        date = date.strip()
        if '야' in date:
            return '2023' + month_dict[month] + date.replace('야', '').replace('()', '').zfill(2) + ' 22:00'
        else:
            return '2023' + month_dict[month] + date.replace('()', '').zfill(2) + ' 12:00'

    df_copy[column] = df_copy[column].astype(str).apply(lambda x: convert_date(x, month))

    # 날짜 열의 데이터 타입을 datetime으로 변경
    df_copy[column] = pd.to_datetime(df_copy[column], format='%Y%m%d %H:%M', errors='coerce')
    return df_copy

def decompose(df, month):
    # '1호기' 열에서 '2호기' 정확히 매치되는 패턴 검색
    df = df.rename(columns = {'1호기': '날짜'})
    pattern = r'^2호기$'
    mask = df['날짜'].apply(lambda x: bool(re.search(pattern, str(x))))
    indices = df[mask].index
    
    # DataFrame을 분할
    dataframes = []
    start_idx = 0
    
    for idx in indices:
        # 현재 인덱스를 새 DataFrame의 시작으로 포함
        dataframes.append(df.iloc[start_idx:idx])
        start_idx = idx
    
    # 마지막 인덱스부터 DataFrame 끝까지 추가
    dataframes.append(df.iloc[start_idx:])

    FirstUnit = dataframes[0]
    SecondUnit = dataframes[1]


    # 1호기 소계, 2호기 소계 추출
    monthly_first = SecondUnit[SecondUnit['날짜']=='1호기소계']
    montyly_second = SecondUnit[SecondUnit['날짜']=='2호기소계']

    # Dataframe 정규화
    FirstUnit = split_dataframe_by_sum(FirstUnit, '날짜')
    FirstUnit = split_dataframe_by_date(FirstUnit, '날짜')
    
    SecondUnit = split_dataframe_by_sum(SecondUnit, '날짜')
    SecondUnit = split_dataframe_by_date(SecondUnit, '날짜')

    # NaN 값을 이전 값으로 채워주기
    FirstUnit = fill_date(FirstUnit)
    SecondUnit = fill_date(SecondUnit)

    # 합계 Dataframe 추출
    FirstUnitTotalSum = FirstUnit[FirstUnit['생산규격']=='합계']
    SecondUnitTotalSum = SecondUnit[SecondUnit['생산규격']=='합계']

    # 날짜 생성 및 포맷 변경
    FirstUnitTotalSum = convert_date_and_format(FirstUnitTotalSum, '날짜', month)
    SecondUnitTotalSum = convert_date_and_format(SecondUnitTotalSum, '날짜', month)
    
    return [FirstUnit, SecondUnit, monthly_first, montyly_second, FirstUnitTotalSum, SecondUnitTotalSum]




def transform_column_name(df):
    df_columns = {
    "날짜": "Date",
    "생산규격": "Production_Standards",
    "현재원": "Current_Staff",
    "작업시간(HR)": "Work_Hours",
    "총투입시간(HR)": "Total_Input_Hours",
    "총작업시간(분)": "Total_Work_Time",
    "휴지시간(비가동HR)": "Idle_Time",
    "순작업시간(가동HR)": "Net_Work_Time",
    "가동율(%)": "Operational_Rate",
    "양품율(%)": "Quality_Rate",
    "생산량(ton)": "Production",
    "투입량(ton)": "Input_Amount",
    "출고량(ton)": "Shipment_Amount",
    "생산총길이(M)": "Total_Production_Length",
    "UPH(M/HR)": "Units_Per_Hour",
    "SPH(천원/HR)": "Sales_Per_Hour",
    "TPH(TON/HR)": "Tons_Per_Hour",
    "MPH(M/HR)": "Meters_Per_Hour"}

    df.rename(columns=df_columns, inplace=True)
    return df

def delete_useless_columns(df):
    df = df.dropna(axis=1, how='all')
    df = df.dropna()
    return df

def index_reset(df):
    df.index = range(len(df))
    df = transform_column_name(df)
    df = delete_useless_columns(df)
    df = df.convert_dtypes()
    return df


def index_reset_v2(df):
    df.index = range(len(df))
    df = transform_column_name(df)
    df = df.convert_dtypes()
    return df

def monthly_df_maker(excel_sheets : dict) -> dict:
    '''
    montly_dict = {'1월' : montly_List, '2월' : montly_List, ...}
    montly_List = [1호기_df, 2호기_df, 1호기 소계, 2호기 소계, 1호기 합계, 2호기 합계]
    '''
    monthly_dict = {}

    try:
        for sheet in excel_sheets:
            result = decompose(excel_sheets[sheet],sheet)
            monthly_dict[sheet] = result
    except Exception as e :
        pass
        # print(sheet)
        # print(e)

    first_unit_df = pd.DataFrame()
    second_unit_df = pd.DataFrame()
    monthly_first = pd.DataFrame()
    monthly_second = pd.DataFrame()
    first_unit_total_sum = pd.DataFrame()
    second_unit_total_sum = pd.DataFrame()
    
    for key in monthly_dict:
        first_unit_df = pd.concat([first_unit_df, monthly_dict[key][0]])
        second_unit_df = pd.concat([second_unit_df, monthly_dict[key][1]])
        monthly_first = pd.concat([monthly_first, monthly_dict[key][2]])
        monthly_second = pd.concat([monthly_second, monthly_dict[key][3]])
        first_unit_total_sum = pd.concat([first_unit_total_sum, monthly_dict[key][4]])
        second_unit_total_sum = pd.concat([second_unit_total_sum, monthly_dict[key][5]]) 

    # Index Reset
    first_unit_df = index_reset_v2(first_unit_df)
    second_unit_df = index_reset_v2(second_unit_df)   
    monthly_first = index_reset(monthly_first)
    monthly_second = index_reset(monthly_second)
    first_unit_total_sum = index_reset(first_unit_total_sum)
    second_unit_total_sum = index_reset(second_unit_total_sum)
    first_unit_total_sum.drop('Production_Standards', axis=1, inplace=True)
    second_unit_total_sum.drop('Production_Standards', axis=1, inplace=True)


    
    
    return [first_unit_df, second_unit_df, monthly_first, monthly_second, first_unit_total_sum, second_unit_total_sum]


# 사용할지 모르는 함수
def save_to_excel(monthly_list):
    for idx, df in enumerate(monthly_list):
        if idx == 0:
            df.to_excel('1호기.xlsx', index=False)
        elif idx == 1:
            df.to_excel('2호기.xlsx', index=False)
        elif idx == 2:
            df.to_excel('1호기 소계.xlsx', index=False)
        elif idx == 3:
            df.to_excel('2호기 소계.xlsx', index=False)
        elif idx == 4:
            df.to_excel('1호기 합계.xlsx', index=False)
        elif idx == 5:
            df.to_excel('2호기 합계.xlsx', index=False)
            
            
            

def save_chart(file_name):
    original_path = 'exports/charts/temp_chart.png'
    new_path = f'html_fig/{file_name}.png'
    shutil.copy(original_path, new_path)
    return None

def bar_scatter_plot(df, title, yaxis_title, color_1='blue', color_2='red'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.values, mode='lines+markers', name='Monthly Production', marker=dict(color=color_1)))
    fig.add_trace(go.Bar(x=df.index, y=df.values, name='Monthly Production', marker=dict(color=color_2)))
    fig.update_layout(yaxis_tickformat='d',
                      title=title,
                      title_x=0.5,  # Center the title
                      xaxis_title='Month',
                      yaxis_title=yaxis_title,
                      showlegend=False,  # Remove the legend
                      autosize=False,  # Disable automatic sizing
                      margin=dict(l=50, r=50, b=100, t=100, pad=10))  # Set margins
    fig_html = pio.to_html(fig, full_html=False)
    # fig.show()
    return fig_html

def bar_scatter_plot_digit(df, title, yaxis_title, color_1='blue', color_2='red'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.values, mode='lines+markers', name='Monthly Production',marker=dict(color=color_1)))
    fig.add_trace(go.Bar(x=df.index, y=df.values, name='Monthly Production', marker=dict(color=color_2)))
    fig.update_layout(
                      title=title,
                      title_x=0.5,  # Center the title
                      xaxis_title='Month',
                      yaxis_title=yaxis_title,
                      showlegend=False,  # Remove the legend
                      autosize=False,  # Disable automatic sizing
                      margin=dict(l=50, r=50, b=100, t=100, pad=10))  # Set margins
    fig_html = pio.to_html(fig, full_html=False)
    # fig.show()
    return fig_html

def pichart(df, title):
    # 'Idle_Time'과 'Net_Work_Time'의 합 계산
    total_time = df[['Idle_Time', 'Net_Work_Time']].sum().sum()

    # 각 값의 비율 계산
    idle_time_ratio = df['Idle_Time'].sum() / total_time
    net_work_time_ratio = df['Net_Work_Time'].sum() / total_time

    # 레이블과 값(비율) 설정
    labels = ['Idle_Time', 'Net_Work_Time']
    values = [idle_time_ratio, net_work_time_ratio]

    # Plotly 파이 차트 생성
    fig = go.Figure(data=go.Pie(labels=labels, values=values))

    # 그래프 설정 업데이트
    fig.update_layout(
        title=title,  # 제목 추가
        title_x=0.5,  # 제목을 중앙으로 이동
        showlegend=False,  # 레전드 제거
        autosize=False,  # 자동 크기 조정 비활성화
        margin=dict(l=50, r=50, b=100, t=100, pad=10)  # 여백 설정
    )

    # 그래프 표시
    fig_html = pio.to_html(fig, full_html=False)
    # fig.show()
    
    return fig_html

def loss_rate_plot(df, title):
    monthly_input_unit_1 = df.resample('M', on='Date')['Input_Amount'].sum()
    monthly_production_unit_1 = df.resample('M', on='Date')['Production'].sum()
    loss = monthly_input_unit_1 - monthly_production_unit_1
    loss_rate = (loss / monthly_input_unit_1) * 100  # 손실률 계산

    fig = go.Figure(data=[
        go.Bar(name='Production', x=monthly_production_unit_1.index, y=monthly_production_unit_1),
        go.Bar(name='Loss', x=loss.index, y=loss),
        go.Scatter(name='Loss Rate', x=loss_rate.index, y=loss_rate, yaxis='y2')  # 손실률 그래프 추가
    ])
    fig.update_layout(
        barmode='stack', 
        title=title,
        xaxis_title='Date',
        yaxis_title='Amount',
        yaxis2=dict(title='Loss Rate (%)', overlaying='y', side='right'),  # 오른쪽 y축 추가
        showlegend=False
    )

    # fig.show()
    fig_html = pio.to_html(fig, full_html=False)
    return fig_html

def make_hr_overview(monthly_list):
    monthly_net_work_unit_1 = monthly_list[4].resample('M', on='Date')['Net_Work_Time'].sum()
    monthly_net_work_unit_2 = monthly_list[5].resample('M', on='Date')['Net_Work_Time'].sum()
    net_work_unit_1 = bar_scatter_plot(monthly_net_work_unit_1, '1호기 Net Work Time', 'Net Work Time(분))')
    net_work_unit_2 = bar_scatter_plot(monthly_net_work_unit_2, '2호기 Net Work Time', 'Net Work Time(분)','red','blue')

    monthly_operational_rate_unit_1 = monthly_list[4].resample('M', on='Date')['Operational_Rate'].mean()
    monthly_operational_rate_unit_2 = monthly_list[5].resample('M', on='Date')['Operational_Rate'].mean()
    operational_rate_unit_1 = bar_scatter_plot_digit(monthly_operational_rate_unit_1, '1호기 Average Operating Rate', 'Operating Rate')
    operational_rate_unit_2 = bar_scatter_plot_digit(monthly_operational_rate_unit_2, '2호기 Average Operating Rate', 'Operating Rate', 'red','blue')

    monthly_input_hours_unit_1 = monthly_list[4].resample('M', on='Date')['Total_Input_Hours'].sum()
    monthly_input_hours_unit_2 = monthly_list[5].resample('M', on='Date')['Total_Input_Hours'].sum()
    input_time_unit_1 = bar_scatter_plot(monthly_input_hours_unit_1, '1호기 Total Input Hours', 'Total Input Hours(시간)')
    input_time_unit_2 = bar_scatter_plot(monthly_input_hours_unit_2, '2호기 Total Input Hours', 'Total Input Hours(시간)','red','blue')

    work_ratio_unit_1 = pichart(monthly_list[4], '1호기 Idle Time vs Net Work Time')
    work_ratio_unit_2 = pichart(monthly_list[5], '2호기 Idle Time vs Net Work Time')

    hr_overview_images = [net_work_unit_1, net_work_unit_2, operational_rate_unit_1, operational_rate_unit_2, input_time_unit_1, input_time_unit_2, work_ratio_unit_1, work_ratio_unit_2]
    
    return hr_overview_images

def make_pr_overview(monthly_list):
    monthly_production_unit_1 = monthly_list[4].resample('M', on='Date')['Production'].sum()
    monthly_production_unit_2 = monthly_list[5].resample('M', on='Date')['Production'].sum()

    monthly_Shipment_Amount_unit_1 = monthly_list[4].resample('M', on='Date')['Shipment_Amount'].sum()
    monthly_Shipment_Amount_unit_2 = monthly_list[5].resample('M', on='Date')['Shipment_Amount'].sum()

    monthly_list[4]['production_per_net_work_time'] = monthly_list[4]['Production'] / monthly_list[4]['Net_Work_Time']
    monthly_list[5]['production_per_net_work_time'] = monthly_list[5]['Production'] / monthly_list[5]['Net_Work_Time']

    monthly_list[4]['production_per_Total_Input_Hours'] = monthly_list[4]['Production'] / monthly_list[4]['Total_Input_Hours']
    monthly_list[5]['production_per_Total_Input_Hours'] = monthly_list[5]['Production'] / monthly_list[5]['Total_Input_Hours']
    
    production_unit_1 = bar_scatter_plot(monthly_production_unit_1, '1호기 Production', 'Production(Ton)')
    production_unit_2 = bar_scatter_plot(monthly_production_unit_2, '2호기 Production', 'Production(Ton)','red','blue')
    shipment_unit_1 = bar_scatter_plot(monthly_Shipment_Amount_unit_1, '1호기 Shipment Amount', 'Shipment Amount(Ton)')
    shipment_unit_2 = bar_scatter_plot(monthly_Shipment_Amount_unit_2, '2호기 Shipment Amount', 'Shipment Amount(Ton)','red','blue')
    production_per_net_work_time_unit_1 = bar_scatter_plot(monthly_list[4].resample('M', on='Date')['production_per_net_work_time'].mean(), '1호기 Production per Net Work Time', 'Production per Net Work Time(Ton/Hour)')
    production_per_net_work_time_unit_2 = bar_scatter_plot(monthly_list[5].resample('M', on='Date')['production_per_net_work_time'].mean(), '2호기 Production per Net Work Time', 'Production per Net Work Time(Ton/Hour)','red','blue')
    production_per_Total_Input_Hours_unit_1 = bar_scatter_plot(monthly_list[4].resample('M', on='Date')['production_per_Total_Input_Hours'].mean(), '1호기 Production per Total Input Hours', 'Production per Total Input Hours(Ton/Hour)')
    production_per_Total_Input_Hours_unit_2 = bar_scatter_plot(monthly_list[5].resample('M', on='Date')['production_per_Total_Input_Hours'].mean(), '2호기 Production per Total Input Hours', 'Production per Total Input Hours(Ton/Hour)','red','blue')

    loss_unit_1 = loss_rate_plot(monthly_list[4], '1호기 Input, Production and Loss over Time')
    loss_unit_2 = loss_rate_plot(monthly_list[5], '2호기 Input, Production and Loss over Time')
    
    pr_overview_images = [production_unit_1, production_unit_2, shipment_unit_1, shipment_unit_2, production_per_net_work_time_unit_1, production_per_net_work_time_unit_2, 
            production_per_Total_Input_Hours_unit_1, production_per_Total_Input_Hours_unit_2, loss_unit_1, loss_unit_2]
    return pr_overview_images

# 그래프 생성
def monthly_hr(df,title):
    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Net_Work_Time'], mode='lines'))

    # 그래프 제목 및 축 레이블 설정
    fig.update_layout(
        title=f'{title} 일별 순 작업시간',
        title_x=0.5,  # 제목을 중간으로 정렬
        xaxis_title='Date',
        yaxis_title='Net_Work_Time(M)'
    )

    # 그래프 출력
    # fig.show()
    net_work_fig_html = pio.to_html(fig, full_html=False)

    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Operational_Rate'], mode='lines'))

    # 그래프 제목 및 축 레이블 설정
    fig.update_layout(
        title=f'{title} 일별 가동율',
        title_x=0.5,  # 제목을 중간으로 정렬
        xaxis_title='Date',
        yaxis_title='Operational_Rate(%)'
    )

    # 그래프 출력
    # fig.show()
    op_rate_fig_html = pio.to_html(fig, full_html=False)
    
    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Total_Input_Hours'], mode='lines'))

    # 그래프 제목 및 축 레이블 설정
    fig.update_layout(
        title=f'{title} 일별 총 작업시간',
        title_x=0.5,  # 제목을 중간으로 정렬
        xaxis_title='Date',
        yaxis_title='Total_Input_Hours(H)'
    )

    # 그래프 출력
    # fig.show()
    total_input_fig_html = pio.to_html(fig, full_html=False)
    
    return [net_work_fig_html, op_rate_fig_html, total_input_fig_html]

def merge_monthly_hr(unit1_df, unit2_df):
    unit_1 = monthly_hr(unit1_df, '1호기')
    unit_2 = monthly_hr(unit2_df, '2호기')
    lst_combined = [item for pair in zip(unit_1, unit_2) for item in pair]
    
    return lst_combined

def make_hr_monthly(monthly_list):
    
    unit_1_grouped = monthly_list[4].groupby(pd.Grouper(key='Date', freq='M'))
    unit_2_grouped = monthly_list[5].groupby(pd.Grouper(key='Date', freq='M'))

    monthly_data_unit_1 = [group for _, group in unit_1_grouped]
    monthly_data_unit_2 = [group for _, group in unit_2_grouped]
    
    hr_monthly_imgaes = []
    for df in zip(monthly_data_unit_1, monthly_data_unit_2):
        hr_monthly_imgaes.append(merge_monthly_hr(df[0], df[1]))
    
    return hr_monthly_imgaes

def monthly_pr(df,title):
    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Production'], mode='lines'))

    # 그래프 제목 및 축 레이블 설정
    fig.update_layout(
        title=f'{title} 일별 생산량',
        title_x=0.5,  # 제목을 중간으로 정렬
        xaxis_title='Date',
        yaxis_title='Production(Ton)'
    )

    # 그래프 출력
    # fig.show()
    product_fig_html = pio.to_html(fig, full_html=False)

    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df['Production']/df['Net_Work_Time'], mode='lines'))

    # 그래프 제목 및 축 레이블 설정
    fig.update_layout(
        title=f'{title} 일별 생산량/순작업시간',
        title_x=0.5,  # 제목을 중간으로 정렬
        xaxis_title='Date',
        yaxis_title='Production/Net_Work_Time(Ton/H)'
    )

    # 그래프 출력
    # fig.show()
    pr_rate_fig_html = pio.to_html(fig, full_html=False)
    
    monthly_input_unit_1 = df['Input_Amount']
    monthly_production_unit_1 = df['Production']
    loss = monthly_input_unit_1 - monthly_production_unit_1
    loss_rate = (loss / monthly_input_unit_1) * 100  # 손실률 계산

    fig = go.Figure(data=[
        go.Bar(name='Production', x=monthly_production_unit_1.index, y=monthly_production_unit_1),
        go.Bar(name='Loss', x=loss.index, y=loss),
        go.Scatter(name='Loss Rate', x=loss_rate.index, y=loss_rate, yaxis='y2')  # 손실률 그래프 추가
    ])
    fig.update_layout(
        barmode='stack', 
        title=f'일별 {title} loss' ,
        xaxis_title='Date',
        yaxis_title='Amount',
        yaxis2=dict(title='Loss Rate (%)', overlaying='y', side='right'),  # 오른쪽 y축 추가
        showlegend=False
    )

    # fig.show()
    loss_fig_html = pio.to_html(fig, full_html=False)

    
    return [product_fig_html, pr_rate_fig_html, loss_fig_html]

def merge_monthly_pr(unit1_df, unit2_df):
    unit_1 = monthly_pr(unit1_df, '1호기')
    unit_2 = monthly_pr(unit2_df, '2호기')
    lst_combined = [item for pair in zip(unit_1, unit_2) for item in pair]
    
    return lst_combined

def make_pr_monthly(monthly_list):
    
    unit_1_grouped = monthly_list[4].groupby(pd.Grouper(key='Date', freq='M'))
    unit_2_grouped = monthly_list[5].groupby(pd.Grouper(key='Date', freq='M'))

    monthly_data_unit_1 = [group for _, group in unit_1_grouped]
    monthly_data_unit_2 = [group for _, group in unit_2_grouped]
    
    pr_monthly_imgaes = []
    for df in zip(monthly_data_unit_1, monthly_data_unit_2):
        pr_monthly_imgaes.append(merge_monthly_pr(df[0], df[1]))
    
    return pr_monthly_imgaes





def make_dashboard(sheets):
    monthly_list = monthly_df_maker(sheets)

    PRIMARY_COLOR = "#0072B5"
    SECONDARY_COLOR = "#B54300"
    pn.extension(design="material", sizing_mode="stretch_width")

    df1_html = monthly_list[2].to_html()  # 1호기 소계
    df2_html = monthly_list[3].to_html()  # 2호기 소계
    df_total_html_unit_1 = monthly_list[4].to_html()  # 1호기 합계
    df_total_html_unit_2 = monthly_list[5].to_html()  # 2호기 합계


    # 파일 경로
    monthly_list = monthly_df_maker(sheets)
    hr_overview_images = make_hr_overview(monthly_list)
    pr_overview_images = make_pr_overview(monthly_list)
    hr_monthly = make_hr_monthly(monthly_list)
    pr_monthly = make_pr_monthly(monthly_list)



    css_style = """
    .nav-item {
        flex-grow: 0;
        flex-shrink: 0;
    }
    td {
        white-space: nowrap;
    }
    """

    # hr_overview_images를 4행 2열로 표시
    hr_overview_images_grid = '<table><tr>{}</tr></table>'.format(
        '</tr><tr>'.join(
            '<td>{}</td>'.format('</td><td>'.join(hr_overview_images[i*2:(i+1)*2])) for i in range(4)
        )
    )
    # pr_overview_images를 4행 2열로 표시
    pr_overview_images_grid = '<table><tr>{}</tr></table>'.format(
        '</tr><tr>'.join(
            '<td>{}</td>'.format('</td><td>'.join(pr_overview_images[i*2:(i+1)*2])) for i in range(5)
        )
    )

    html_template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TPC Global</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <style>
            {css_style}
        </style>
    </head>
    <body>
        <h1>TPC Global</h1>
        <div class="container-fluid">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#hr">인적자원</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#production">생산관련</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#subtotal1">1호기 소계</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#subtotal2">2호기 소계</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#total1">1호기 일별 합계</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#total2">2호기 일별 합계</a>
                </li>
            </ul>
            <div class="tab-content">
                <div class="tab-pane active" id="hr">
                    <ul class="nav nav-tabs">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#hr_overview">개요</a>
                        </li>
                        {"".join('<li class="nav-item"><a class="nav-link" data-toggle="tab" href="#hr_monthly_{}">{}</a></li>'.format(i+1, i+1) for i in range(12))}  <!-- 각 월의 탭 추가 -->
                    </ul>
                    <div class="tab-content">
                        <div class="tab-pane active" id="hr_overview">
                            {hr_overview_images_grid}
                        </div>
                        {"".join('<div class="tab-pane" id="hr_monthly_{}"><table><tr><td>{}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td></tr></table></div>'.format(i+1, hr_monthly[i][0], hr_monthly[i][1], hr_monthly[i][2], hr_monthly[i][3], hr_monthly[i][4], hr_monthly[i][5]) for i in range(len(hr_monthly)))}  <!-- 각 월의 이미지 추가 -->
                    </div>
                </div>
                <div class="tab-pane" id="production">
                    <ul class="nav nav-tabs">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#production_overview">개요</a>
                        </li>
                            {"".join('<li class="nav-item"><a class="nav-link" data-toggle="tab" href="#pr_monthly_{}">{}</a></li>'.format(i+1, i+1) for i in range(12))}  <!-- 각 월의 탭 추가 -->

                    </ul>
                    <div class="tab-content">
                        <div class="tab-pane active" id="production_overview">
                            {pr_overview_images_grid}  <!-- pr_overview_images_grid 삽입 -->
                        </div>
                        {"".join('<div class="tab-pane" id="pr_monthly_{}"><table><tr><td>{}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td></tr><tr><td>{}</td><td>{}</td></tr></table></div>'.format(i+1, pr_monthly[i][0], pr_monthly[i][1], pr_monthly[i][2], pr_monthly[i][3], pr_monthly[i][4], pr_monthly[i][5]) for i in range(len(pr_monthly)))}  <!-- 각 월의 이미지 추가 -->

                    </div>
                </div>
                <div class="tab-pane" id="subtotal1">
                    {df1_html}
                </div>
                <div class="tab-pane" id="subtotal2">
                    {df2_html}
                </div>
                <div class="tab-pane" id="total1">
                    {df_total_html_unit_1}
                </div>
                <div class="tab-pane" id="total2">
                    {df_total_html_unit_2}
                </div>
            </div>
        </div>
        <!-- Bootstrap JavaScript -->
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''
    with open('TPC_GLOBAL.html', 'w') as f:
        f.write(html_template)
    
    return html_template

if __name__ == '__main__':
    file_path = '2023_data.xlsx'
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    sheets = {sheet_name: xls.parse(sheet_name, header=3) for sheet_name in xls.sheet_names}
    html_file = make_dashboard(sheets)