#
# Python Script to Illustrate
# Financial Time Series Storage with
# the TsTables Package
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import tstables
import datetime
import tables as tb
from sample_data import generate_sample_data

# sample data generation
data = generate_sample_data(rows=2.5e6, cols=5, freq='1s').round(2)


class desc(tb.IsDescription):
    ''' Description of TsTables table structure.
    '''
    timestamp = tb.Int64Col(pos=0)
    No0 = tb.Float64Col(pos=1)
    No1 = tb.Float64Col(pos=2)
    No2 = tb.Float64Col(pos=3)
    No3 = tb.Float64Col(pos=4)
    No4 = tb.Float64Col(pos=5)


# creating the TsTables table object
h5 = tb.open_file('data.h5', 'w')
ts = h5.create_ts('/', 'data', desc)

# appending the data to the table object
ts.append(data)
print(data.info())
start = datetime.datetime(2017, 1, 2)
end = datetime.datetime(2017,1, 3)
print(ts.read_range(start, end))
h5.close()
