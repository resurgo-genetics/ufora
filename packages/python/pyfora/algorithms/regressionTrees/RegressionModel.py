#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import pyfora.algorithms.regressionTrees.RegressionTree as RegressionTree


class RegressionModel:
    """A class representing a gradient-boosted regression tree model 
    fit to data.

    """
    def __init__(
            self,
            additiveRegressionTree,
            X,
            XDimensions,
            yAsSeries,
            loss,
            regressionTreeBuilder,
            learningRate
            ):
        self.additiveRegressionTree = additiveRegressionTree
        self.X = X
        self.XDimensions = XDimensions
        self.yAsSeries = yAsSeries
        self.loss = loss
        self.regressionTreeBuilder = regressionTreeBuilder
        self.learningRate = learningRate

    def score(self, X, yTrue):
        raise NotImplementedError()

    def predict(self, df, nEstimators=None):
        """Use the `RegressionModel` `self` to predict on the 
        `pandas.DataFrame` `df`.
        
        """
        return self.additiveRegressionTree.predict(df, nEstimators)

    def predictWithPreviousResult(self, previousPredictions, df):
        return previousPredictions + self.additiveRegressionTree.getTree(-1).predict(df)

    def pseudoResidualsAndPredictions(self, previousPredictions):
        if previousPredictions is None:
            predictions = self.predict(self.X)
        else:
            predictions = self.predictWithPreviousResult(previousPredictions, self.X)

        return self.loss.negativeGradient(self.yAsSeries, predictions), predictions

    @staticmethod
    def getInitialModel(X, yAsSeries, loss, learningRate, treeBuilderArgs):
        additiveRegressionTree = loss.initialModel(yAsSeries)
        XDimensions = range(X.shape[1])
        baseModelBuilder = RegressionTree.RegressionTreeBuilder(
            treeBuilderArgs.maxDepth,
            treeBuilderArgs.impurityMeasure,
            treeBuilderArgs.minSamplesSplit,
            treeBuilderArgs.numBuckets
            )
        
        if loss.needsOriginalYValues:
            X = X.pyfora_addColumn("__originalValues", yAsSeries)

        return RegressionModel(
            additiveRegressionTree,
            X,
            XDimensions,
            yAsSeries,
            loss,
            baseModelBuilder,
            learningRate
            )

    def boost(self, predictions, pseudoResiduals):
        localX = self.X
        targetDim = localX.shape[1]
        
        localX = localX.pyfora_addColumn("__pseudoResiduals", pseudoResiduals)

        if self.loss.needsPredictedValues:
            localX = localX.pyfora_addColumn("__predictedValues", predictions)

        nextRegressionTree = self.regressionTreeBuilder.fit_(
            localX,
            targetDim,
            None,
            self.XDimensions,
            self.loss.leafValueFun(self.learningRate),
            None)

        return RegressionModel(
            self.additiveRegressionTree + nextRegressionTree,
            self.X,
            self.XDimensions,
            self.yAsSeries,
            self.loss,
            self.regressionTreeBuilder,
            self.learningRate)

    def featureImportances(self):
        raise NotImplementedError()




