import pandas as pd
import ascertainment as asc
import datetime as dt
import us


class CountyRisk:

    def __init__(self):
        print('reading counties')
        self.counties = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

        print('getting ensemble forecasts')
        # TODO: change this to fetch from the URL on GitHub https://github.com/reichlab/covid19-forecast-hub/blob/master/data-processed/COVIDhub-ensemble/2021-02-15-COVIDhub-ensemble.csv
        self.forecasts = pd.read_csv("C:\\Users\\jadaf\\Desktop\\Contact-Tracing\\2021-02-15-COVIDhub-ensemble.csv")

        today_d = pd.to_datetime(self.counties.date).max()
        today_d -= dt.timedelta(days=today_d.weekday() % 5) ## subtract weekday to get to saturday which is 5
        print(type(today_d))
        self.today = dt.datetime.strftime(today_d, '%Y-%m-%d')
        self.past = dt.datetime.strftime(today_d - dt.timedelta(days=7), '%Y-%m-%d')
        print(self.forecasts.head())
        self.three_weeks = dt.datetime.strftime(today_d + dt.timedelta(days=21), '%Y-%m-%d')
        self.two_weeks = dt.datetime.strftime(today_d + dt.timedelta(days=14), '%Y-%m-%d')

        #s = self.counties.set_index('date')
        s = self.forecasts.set_index('target_end_date')  # a little different situation here??
        s.rename(columns={"location": "fips", "value": "cases"}, inplace=True)
        self.all_fips = s.fips.dropna().unique()
        print(s.index)
        #self.active_cases = dict((fips, s[s.fips == fips].cases[self.today] - s[s.fips == fips].cases[self.past]) for fips in self.all_fips)
        #for fips in self.all_fips:
        #    print(fips)
        #    print(s[s.fips == fips])
        #    print(s[s.fips == fips].cases[self.three_weeks])
        #    print(s[s.fips == fips].cases[self.two_weeks])
        self.active_cases = dict((fips, s[s.fips == fips].cases[self.three_weeks] - s[s.fips == fips].cases[self.two_weeks]) for fips in self.all_fips)

        print('reading county populations')
        pop_csv = pd.read_csv('https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv', encoding='latin1')
        pop_csv['FIPS'] = pop_csv.STATE * 1000 + pop_csv.COUNTY
        self.pop = pop_csv.set_index('FIPS')['POPESTIMATE2019']

        self.ascertainment = asc.Ascertainment(today_d + dt.timedelta(days=21), pd.to_datetime(self.past) + dt.timedelta(days=21))
    
    def risk(self, county_fips: int, event_size: int, date: dt.datetime) -> float:
        state_fips = str(county_fips // 1000)
        if len(state_fips) == 1: state_fips = '0' + state_fips
        I = self.active_cases[county_fips] * self.ascertainment.ratio_state(us.states.lookup(state_fips).name)
        N = self.pop[county_fips]
        p = I / N
        return 1 - (1 - p) ** event_size
