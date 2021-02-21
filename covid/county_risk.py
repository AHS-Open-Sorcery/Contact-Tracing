import pandas as pd
import ascertainment as asc
import datetime as dt
import us


def floor_to_sat(date: dt.date):
    wd = date.weekday()
    days_back = 0
    if 0 <= wd <= 1:
        days_back = wd + 2
    if 2 <= wd <= 4:
        days_back = -5 + wd
    if wd == 6:
        days_back = 1
    return date - dt.timedelta(days=days_back)


class CountyRisk:

    def __init__(self):
        print('reading counties')
        self.counties = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

        print('getting ensemble forecasts')
        self.forecasts = pd.read_csv("https://raw.githubusercontent.com/reichlab/covid19-forecast-hub/master/data-processed/COVIDhub-ensemble/2021-02-15-COVIDhub-ensemble.csv")

        today_d = pd.to_datetime(self.counties.date).max()
        today_d -= dt.timedelta(days=today_d.weekday() % 5) ## subtract weekday to get to saturday which is 5


        self.today = dt.datetime.strftime(today_d, '%Y-%m-%d')
        self.past = dt.datetime.strftime(today_d - dt.timedelta(days=7), '%Y-%m-%d')

        self.three_weeks = dt.datetime.strftime(today_d + dt.timedelta(days=21), '%Y-%m-%d')
        self.two_weeks = dt.datetime.strftime(today_d + dt.timedelta(days=14), '%Y-%m-%d')

        #s = self.counties.set_index('date')
        self.fore = self.forecasts
        self.fore.rename(columns={"location": "fips", "value": "cases"}, inplace=True)
        self.all_fips = self.fore.fips.dropna().unique()
        #self.active_cases = dict((fips, s[s.fips == fips].cases[self.today] - s[s.fips == fips].cases[self.past]) for fips in self.all_fips)
        #for fips in self.all_fips:
        #    print(fips)
        #    print(s[s.fips == fips])
        #    print(s[s.fips == fips].cases[self.three_weeks])
        #    print(s[s.fips == fips].cases[self.two_weeks])
        # self.active_cases = dict((fips, s[s.fips == fips].cases[self.three_weeks] - s[s.fips == fips].cases[self.two_weeks]) for fips in self.all_fips)

        print('reading county populations')
        pop_csv = pd.read_csv('https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv', encoding='latin1')
        pop_csv['FIPS'] = pop_csv.STATE * 1000 + pop_csv.COUNTY
        self.pop = pop_csv.set_index('FIPS')['POPESTIMATE2019']

        self.ascertainment = asc.Ascertainment(today_d, pd.to_datetime(self.past))


    def location_cases(self, fips: int, date: dt.date):
        return self.fore[(self.fore.fips == str(fips)) &
                         (self.fore.target_end_date == date.isoformat()) &
                         (self.fore.type == 'point')].cases.iloc[0]

    def risk(self, county_fips: int, event_size: int, date: dt.date) -> float:
        sat_date = floor_to_sat(date)
        past_sat_date = sat_date - dt.timedelta(days=7)
        print(sat_date, past_sat_date)
        case_growth = (self.location_cases(county_fips, sat_date)) / 7 * 10

        print(case_growth)

        state_fips = str(county_fips // 1000)
        if len(state_fips) == 1:
            state_fips = '0' + state_fips
        I = case_growth * self.ascertainment.ratio_state(us.states.lookup(state_fips).name)
        N = self.pop[county_fips]
        p = I / N
        return 1 - (1 - p) ** event_size
