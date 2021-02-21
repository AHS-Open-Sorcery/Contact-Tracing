from covid import county_risk
from event import Event

cr = county_risk.CountyRisk()


def event_risk(evt: Event, est_seats: int) -> float:
    print(f'cr.risk({evt.fips}, {est_seats}, {evt.date})')
    return cr.risk(evt.fips, est_seats, evt.date)
