include('svg11.fan')

# where (int(<width_value>) > 1e8 or int(<height_value>) > 1e8)

# Check with extreme number values
where <Number_datatype> == "'1000000'"

# Ensure we have a minimum of children
where len(<svg>) > 20