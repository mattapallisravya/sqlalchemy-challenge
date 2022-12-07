# sqlalchemy-challenge
- Worked on Hawaii SQL lite database which has two tables measurement and station. 
- Dataset has data related to climate of hawaii from 2010 to 2017. 
- Designed an application to check the weather of hawaii between the given dates or the given date to end date.

Part 1: Analysis and Exploration of Climate Data
- used SQLAlchemy ORM queries, Pandas, and Matplotlib.
- Found the most recent date in dataset and calculated the precipitation data for the one year.
- Created the histogram plot that shows how precipitation varies.
- Created query to find most active station and calculated the temperature stats for one year back from latest date.
- Ploted the results as histogram with bins of 12.

Part 2: Designing Climate App
- Used flask, SQL alchemy.
- Defined the flask API based on the analysis done.
- App has home page which lists all the available routes and how to use them.

Static Routes:

- Precipitation route:
    - Gives the information about precipitation data for past 12 months from the latest date in dataset.
    - Returns Json representation of date and precipitation in the form of dictionary.

- Station route: 
    - Returns all the available stations list in the dataset.

- Temperature route:
    - Returns dates and temperature observations of the most-active station for the previous year of data.
    
- API Dynamic Route:

- Start route:
      - Accepts the start date as a parameter from the URL.

      - Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset.
      
- Start/End route:
      - Accepts the start and end dates as parameters from the URL.

      - Returns the min, max, and average temperatures calculated from the given start date to the given end date.











