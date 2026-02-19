"""Schema definitions for job configuration validation"""

from datetime import date
from enum import UNIQUE, Enum, verify
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


@verify(UNIQUE)
class Source(str, Enum):
    """Enum for different feature data sources"""

    MACRO = "macro"
    EQUITIES = "equities"
    CUSTOM = "custom"


@verify(UNIQUE)
class ModelType(Enum):
    """Enum for different model types"""

    RANDOM_FOREST = "random_forest"
    LINEAR_REGRESSION = "linear_regression"


@verify(UNIQUE)
class MetricType(Enum):
    """Enum for what we are predicting for our asset (i.e. our y)"""

    RETURN = "return"
    VOLATILITY = "volatility"
    PRICE = "price"


@verify(UNIQUE)
class Lag(Enum):
    """How many horizon units forward the model looks"""

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


@verify(UNIQUE)
class Horizon(Enum):
    """Enum for different horizons"""

    DAILY = "daily"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BIANNUALLY = "biannually"


class Asset(BaseModel):
    """Represents a tradable asset"""

    symbol: str = Field(
        ...,
        min_length=1,
        description="Asset ticker symbol (e.g., 'AAPL', 'BTCUSD')",
    )
    source: Source = Field(default=Source.MACRO, description="Source of the asset data")
    horizon: Horizon = Field(
        default=Horizon.MONTHLY, description="Horizon of the model"
    )
    lag: Lag = Field(
        default=Lag.ONE, description="How many units forward-looking to train the model"
    )
    metric: MetricType = Field(
        default=MetricType.RETURN,
        description="Metric that we are going to predict for our asset.",
    )


class FeatureDef(BaseModel):
    """Definition of a single feature transformation for a field."""

    func: str = Field(
        "self",
        description="Transformation function (e.g., 'return', 'zscore', 'self')",
    )
    params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional parameters for the feature (e.g., window size, decay rate)",
    )


class DataField(BaseModel):
    """Represents a data field (macro or equity) and its associated features."""

    field: str = Field(..., description="Field name (e.g., 'PX_LAST', 'FEDFUNDS')")
    features: List[FeatureDef] = Field(
        default_factory=lambda: [FeatureDef(func="self")],
        description="List of features to compute for this field.",
    )


class MacroData(BaseModel):
    """Macroeconomic data configuration"""

    fields: List[DataField] = Field(
        default_factory=list, description="Macro fields with their features"
    )


class EquitiesData(BaseModel):
    """Equity data configuration with fields per symbol."""

    symbol_fields: Dict[str, List[DataField]] = Field(
        default_factory=dict,
        description="Mapping of symbol -> list of fields and their features",
    )


class CustomData(BaseModel):
    """Materialized / compound views configuration"""

    fields: List[DataField] = Field(
        default_factory=list,
        description="List of fields and feature definitions for this custom data source",
    )


class Data(BaseModel):
    """Data sources configuration"""

    macro: Optional[MacroData] = Field(
        default=None, description="Macro-economic data configuration"
    )
    equities: Optional[EquitiesData] = Field(
        default=None, description="Security-specifc data configuration"
    )
    custom: Optional[Dict[str, CustomData]] = Field(
        default=None, description="Compound features data configuration"
    )


class ModelSpec(BaseModel):
    """Machine learning model configuration"""

    mtype: ModelType = Field(
        ...,
        description="Model type identifier",
    )
    params: Optional[Dict[str, Any]] = Field(
        default={},
        description="Model configuration settings",
    )


class Timeframe(BaseModel):
    """Time interval for training and testing"""

    start: date = Field(..., description="Start date (inclusive)")
    end: date = Field(..., description="End date (inclusive)")

    @model_validator(mode="after")
    def check_order(self) -> "Timeframe":
        """Ensure that the timeframe is valid"""
        if self.end < self.start:
            raise ValueError(
                f"Invalid timeframe: end date {self.end} is earlier than start date {self.start}"
            )
        return self


class Metadata(BaseModel):
    """Metadata describing the job"""

    owner: str = Field(..., min_length=1, description="Owner of the job")
    description: str = Field(..., description="Job description or notes")


class Configuration(BaseModel):
    """Top-level schema describing a full model specification"""

    asset: Asset
    data: Data = Field(..., description="Data sources configuration")
    model: ModelSpec
    normalize: bool = Field(
        default=False,
        description="Whether to normalize all data (macro, equities, views) before feature computation",
    )
    timeframe: Timeframe
    metadata: Metadata