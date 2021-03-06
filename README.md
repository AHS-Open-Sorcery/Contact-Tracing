# Open Sorcery: Smart COVID-19 Event Planner

**Problem:** During the pandemic, we're all trying our best to avoid going out -- but sometimes, it's impossible to avoid. To be as safe as possible, we need many different types of information: how to set up as safely as possible, how to contact-trace, and how much risk is involved in a given event.

**Solution:** In those situations, having a way to easily contact-trace, plan a socially distanced layout, and calculate risk is important. So we made the Smart COVID-19 Event Planner, which helps us figure out many of these factors.

**Features:**
* Layout planning: Our drag-and-drop front-end interface allows the event planner to customize the layout of the event. There will also be an option to automatically configure the layout for maximum social distancing.
* Event management: Event planners will have the option to invite guests to their event using a custom invite link. Guests can view the risk (see below) and make an informed decision before they RSVP. 
* Risk calculation: Both event planners and guests will be able to view the risk that someone at the event will be positive for covid-19 based on the most current case data for the county in question. 
* Contact tracing: We will save the data from the layout for easier contact tracing after the event, if necessary. 

**Libraries/Data Sources Used:**
* Libraries:
  * MaterializeCSS - style sheet for frontend
  * JQuery - general frontend support
  * Pandas - for data table processing
  * NumPy - to cooperate with pandas
  * Python Datetime - to process all the dates in the data
  * us - for state information
  * Jinja - integrating frontend and backend
  * Blacksheep - integrating frontend and backend

* Sources of Data:
  * [JHU COVID-19 dataset](https://github.com/CSSEGISandData/COVID-19)
  * [New York Times COVID-19 Data](https://github.com/nytimes/covid-19-data)
  * [Reich Lab Ensemble Forecast Data](https://github.com/reichlab/covid19-forecast-hub/blob/master/data-processed/COVIDhub-ensemble/2021-02-15-COVIDhub-ensemble.csv)
  * [Census Data](www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv)
