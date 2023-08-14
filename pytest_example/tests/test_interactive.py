import numpy as np
import pytest

from .. import interactive


# format of a test
 def test_name_of_test():
    - create 'mock' data
    - create the expected output: this is known to be the correct result.
    - call the function you want to test. create the function output.
    
    assert expected_output == function_output







def test_get_uncert_from_cov_matrix():
    matrix = np.array([[0.5, 0.1], [0.3, 0.3]])
    diags = (np.sqrt(0.5), np.sqrt(0.3))

    uncert = interactive.get_uncert_from_cov_matrix(matrix)
    assert diags[0] == uncert[0]
    assert diags[1] == uncert[1]


#def test_get_uncert_from_cov_matrix_single_value():
#    matrix = 5
#    diags = np.sqrt(5)
#
#    uncert = interactive.get_uncert_from_cov_matrix(matrix)
#    assert diags == uncert


#def test_powerlaw():
#   pass 


