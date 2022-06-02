import pandas as pd
from LeastSquare import calculateError


class UnitTest():
    def setUp(self):
        # Setting dummy data
        firstDataSet = {"x":[8.0,14.0,22.0],"y":[4.0,7.0,5.0]}
        secondDataSet = {"x":[1.0,2.0,3.0], "y":[7.0,8.0,9.0]}

        self.firstDataFrame = pd.DataFrame(data=firstDataSet)
        self.secondDataframe = pd.DataFrame(data=secondDataSet)

    def testErrorSquared(self):
        # check to see first function correct value
        self.assertEqual(calculateError(self.firstFunction, self.secondFunction), 40.0)
        # check to test the loss function value
        self.assertEqual(calculateError(self.secondFunction, self.firstFunction), 14.0)
        # test to check that regression is zero or not
        self.assertEqual(calculateError(self.firstFunction, self.firstFunction), 0.0)