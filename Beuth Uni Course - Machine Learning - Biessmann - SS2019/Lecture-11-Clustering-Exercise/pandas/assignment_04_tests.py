import assignment_04 as a
import numpy as np
import pandas as pd

df = pd.read_csv("data/zuwendungen-berlin.csv.gz")

def assignment_04_01_test():
    spending_statistics = np.array(
            [4.08200000e+04, 2.29215965e+05, 3.93196343e+06, 1.00000000e+02,
            4.67300000e+03, 1.64770000e+04, 6.11755000e+04, 4.87261162e+08])
    assert np.allclose(a.assignment_04_01(df), spending_statistics)

def assignment_04_02_test():
    result = sorted(a.assignment_04_02(df))
    assert (result[0] == "Rock 'n' Roll Club Pinguin Berlin e. V.") & \
                (result[1] == 'Triathlongemeinschaft Sisu Berlin e. V.')

def assignment_04_03_test():
    correct = np.array([500.0, 115557.5, 41852102.0])
    assert np.array_equal(a.assignment_04_03(df), correct)

def assignment_04_04_test():
    ubahn_cost_ranking = ['U5', 'U2', 'U1', 'U6', 'U8', 'U7', 'U9', 'U3', 'U4']
    assert all([x==y for x,y in zip(a.assignment_04_04(df),ubahn_cost_ranking)])

if __name__ == '__main__':
    assignment_04_01_test()
    assignment_04_02_test()
    assignment_04_03_test()
    assignment_04_04_test()
