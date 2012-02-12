datio
======
*datio* is data processing library useful in simulation work.

The main class, Series, was designed to access data by rows or columns.

Series is useful in simulation work where you need to process each 
row of data while analyzing the last x items for a given column.

For example, in stock simulations, you'll iterate through all the
prices for a stock but for each price period calculate the 20 period moving
average of the closing price.  The class, Series, makes the work of
reading by rows while processing columns easy.


Overview
--------
The major functions of datio:

* **Series():**
    Access data across rows or columns. Append by rows or columns.
    Update Series in place.
    
* **lol2dol():**
    convert a list of lists to dict of lists. Basically move from
    accessing data by rows to accessing data by columns.
    
* **csv2lol():**
    load data from a csv file to a list of lists.
    
* **format_values():**
    convert a list of values from one type to another such as float,
    int, string, or datatime.strptime.


License
-------
Made available under the MIT License.


Usage
-----
Import the library:
    >>> import datio

Define some data to work with:
    >>> prices_lol = []
    >>> prices_lol.append(['1997-01-01', 'goog', '32.00'])
    >>> prices_lol.append(['1997-01-02', 'goog', '33.00'])
    >>> prices_lol.append(['1997-01-03', 'goog', '34.00'])

Load the data into your series:
    >>> series = datio.Series('dates', 'symbols', 'closes')
    >>> series.from_values(prices_lol)

Access all the dates in the series:
    >>> series.dates
    ['1997-01-01', '1997-01-02', '1997-01-03']
    
Access only the 2nd row of the series:
    >>> series[1]
    ('1997-01-02', 'goog', '33.00')

Access the 1st row of the series for the closes column:
    >>> series.closes[0]
    '32.00'

Format the closes column to float:
    >>> series.format('closes', float)
    [32.0, 33.0, 34.0]

We'd like to include price opens as well.  So, append opens to series:
    >>> series.appendcol('opens', [31.00, 33.0, 35])
    >>> series.opens
    [31.0, 33.0, 35]

We'll probably need a column for storing moving averages later on:
    >>> series.initcol('sma_closes')
    >>> series.sma_closes
    [None, None, None]

Now, we'd like to add a row for the 1997-01-04 price period:
    >>> series.append(['1997-01-04', 'goog', 38, 37])
    >>> series[3]
    ('1997-01-04', 'goog', 38, 37, None)
    
As you can see, the sma_closes column is None since we didn't include it in the appended values.  So, let's change that to 0.0:
    >>> series.sma_closes[3] = 0.0

Let's format the dates column to datetime:
    >>> series.format('dates', datetime.strptime, '%Y-%m-%d')
    >>> series.dates[0].__str__()
    '1997-01-01 00:00:00'

Finally, let's sort the series from high to low closing price:
    >>> series.sort('closes', order='d')
    >>> series.closes
    [38, 34.0, 33.0, 32.0]

Roadmap
-------
* Not sure if I want the columns to adhere to the last format call made for all future values appended?
* Really don't like the fact that columns can be updated outside of the series.  But, not sure if turning them into tuples is a good thing cause of overhead of needing to turn back to lists to update within series.
* Considering having the rows from the call be namedtuples instead of tuples. This would allow named attribute access and I believe lower overhead?  But, at this point, don't have a true need for this feature.


Contact
-------
For additional information, please email:
    mike@taylortree.com
