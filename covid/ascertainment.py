import pandas as pd
import datetime as dt

class Ascertainment:
    fmt_date = lambda date: dt.datetime.strftime(date - dt.timedelta(days=21), '%m-%d-%Y')
    print(fmt_date)
    csv_loc = lambda date: f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{Ascertainment.fmt_date(date)}.csv'
    
    def __init__(self, today: dt.datetime, past: dt.datetime) -> None:
        self.today = today
        self.past = past
        print('downloading JHU reports')
        self.today_report = pd.read_csv(Ascertainment.csv_loc(today))
        self.past_report = pd.read_csv(Ascertainment.csv_loc(past))

    def ratio_state(self, state: str) -> float:
        conf_total = lambda df: df[df.Province_State == state][['Confirmed', 'Total_Test_Results', 'Deaths']].iloc[0]
        today_conf_total = conf_total(self.today_report)
        past_conf_total = conf_total(self.past_report)
        dConfirmed = (today_conf_total.Confirmed - past_conf_total.Confirmed)
        pos_rate = dConfirmed / (today_conf_total.Total_Test_Results - past_conf_total.Total_Test_Results)
        # death_div_cases = (today_conf_total.Deaths - past_conf_total.Deaths) / dConfirmed
        # From YYG
        day_i = (self.today - dt.timedelta(days=(self.today - self.past).days // 2) - pd.to_datetime('2020-02-01')).days
        prevratio = 1000 / (day_i + 50) * pos_rate**0.5 + 2
        return prevratio
