import pandas as pd
import ascertainment as asc
import datetime as dt
import us

class CountyRisk:

    def __init__(self):
        print('reading counties')
        self.counties = pd.read_csv('us-counties.csv')
        today_d = pd.to_datetime(self.counties.date).max()
        self.today = dt.datetime.strftime(today_d, '%Y-%m-%d')
        self.past = dt.datetime.strftime(today_d - dt.timedelta(days=10), '%Y-%m-%d')

        s = self.counties.set_index('date')
        self.all_fips = s.fips.dropna().unique()
        self.active_cases = dict((fips, s[s.fips == fips].cases[self.today] - s[s.fips == fips].cases[self.past]) for fips in self.all_fips)

        print('reading county populations')
        pop_csv = pd.read_csv('counties.csv')
        pop_csv['FIPS'] = pop_csv.STATE * 1000 + pop_csv.COUNTY
        self.pop = pop_csv.set_index('FIPS')['POPESTIMATE2019']

        self.ascertainment = asc.Ascertainment(today_d, pd.to_datetime(self.past))
    
    def risk(self, county_fips: int, event_size: int, date: dt.datetime) -> float:
        state_fips = str(county_fips // 1000)
        if len(state_fips) == 1: state_fips = '0' + state_fips
        I = self.active_cases[county_fips] * self.ascertainment.ratio_state(us.states.lookup(state_fips).name)
        N = self.pop[county_fips]
        p = I / N
        return 1 - (1 - p) ** event_size