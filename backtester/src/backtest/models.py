"""Linear regression model implementation."""

import pickle
from io import BytesIO
from typing import Optional, override

import pandas as pd
from sklearn.linear_model import LinearRegression

class LinearRegression():
    """Linear regression model implementation."""

    model: Optional[LinearRegression]

    @override
    def fit(self, x: pd.DataFrame, y: pd.Series) -> None:
        """
        Fit the model to the training data.
        Args:
            x (pd.DataFrame): Training x data.
            y (pd.Series): Training y data.

        Returns: None
        """
        self.model = LinearRegression()
        self.model.fit(x, y)

    @override
    def predict(self, x: pd.DataFrame) -> pd.Series:
        """
        Use the model to predict on test data.
        Args:
            x (pd.DataFrame): Test data to predict on.

        Returns: (pd.Series) Predicted output.
        """
        if self.model is not None:
            preds = self.model.predict(x)
            return pd.Series(preds, index=x.index)
        raise ValueError("Model not defined.")

    @override
    def save(self, buffer: BytesIO) -> None:
        """
        Save the model into the provided buffer.
        Args:
            buffer (BytesIO): The buffer to write to

        Returns: None
        """
        if self.model is not None:
            pickle.dump(self.model, buffer)