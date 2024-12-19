from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import numpy as np
from scipy import stats

@dataclass
class ConfidenceScore:
    """Represents a confidence assessment with detailed metrics."""
    score: float  # Overall confidence score (0-1)
    factors: Dict[str, float]  # Individual factor scores
    uncertainty: float  # Uncertainty measure (0-1)
    reliability: float  # Data reliability score (0-1)
    sample_size: int  # Number of data points considered

class ConfidenceAnalyzer:
    """Analyzes and scores confidence levels in decisions and predictions."""

    def __init__(self, min_sample_size: int = 5):
        """Initialize the confidence analyzer.

        Args:
            min_sample_size: Minimum sample size for full confidence
        """
        self.min_sample_size = min_sample_size
        self.weight_factors = {
            'data_quality': 0.3,
            'consistency': 0.2,
            'statistical_significance': 0.2,
            'sample_size': 0.15,
            'time_relevance': 0.15
        }

    def evaluate_confidence(self, data: Dict[str, Any]) -> ConfidenceScore:
        """Evaluate confidence level based on provided data.

        Args:
            data: Dictionary containing:
                - values: List of numerical values or observations
                - metadata: Additional context and quality indicators
                - timestamp: Optional timestamp for time relevance

        Returns:
            ConfidenceScore object with detailed metrics
        """
        factors = {}
        
        # Evaluate data quality
        factors['data_quality'] = self._assess_data_quality(data)
        
        # Evaluate consistency
        factors['consistency'] = self._assess_consistency(data)
        
        # Evaluate statistical significance
        factors['statistical_significance'] = self._assess_statistical_significance(data)
        
        # Evaluate sample size adequacy
        factors['sample_size'] = self._assess_sample_size(data)
        
        # Evaluate time relevance
        factors['time_relevance'] = self._assess_time_relevance(data)
        
        # Calculate overall confidence score
        overall_score = sum(score * self.weight_factors[factor]
                           for factor, score in factors.items())
        
        # Calculate uncertainty
        uncertainty = self._calculate_uncertainty(factors)
        
        # Calculate reliability
        reliability = self._calculate_reliability(factors)
        
        return ConfidenceScore(
            score=overall_score,
            factors=factors,
            uncertainty=uncertainty,
            reliability=reliability,
            sample_size=len(data.get('values', []))
        )

    def _assess_data_quality(self, data: Dict[str, Any]) -> float:
        """Assess the quality of input data."""
        quality_score = 1.0
        metadata = data.get('metadata', {})
        
        # Check for missing values
        values = data.get('values', [])
        if not values:
            return 0.0
            
        missing_ratio = sum(1 for v in values if v is None) / len(values)
        quality_score *= (1 - missing_ratio)
        
        # Check for data validation flags
        if metadata.get('validation_errors', []):
            quality_score *= 0.7
            
        # Consider data source reliability
        source_reliability = metadata.get('source_reliability', 1.0)
        quality_score *= source_reliability
        
        return quality_score

    def _assess_consistency(self, data: Dict[str, Any]) -> float:
        """Assess data consistency and stability."""
        values = data.get('values', [])
        if not values:
            return 0.0
            
        # Convert to numpy array and remove None values
        values = np.array([v for v in values if v is not None])
        if len(values) < 2:
            return 0.5
            
        # Calculate coefficient of variation
        cv = np.std(values) / np.mean(values) if np.mean(values) != 0 else 1.0
        consistency_score = 1 / (1 + cv)
        
        # Check for outliers
        z_scores = np.abs(stats.zscore(values))
        outlier_ratio = np.sum(z_scores > 3) / len(values)
        consistency_score *= (1 - outlier_ratio)
        
        return consistency_score

    def _assess_statistical_significance(self, data: Dict[str, Any]) -> float:
        """Assess statistical significance of the data."""
        values = data.get('values', [])
        if not values:
            return 0.0
            
        # Convert to numpy array and remove None values
        values = np.array([v for v in values if v is not None])
        if len(values) < 2:
            return 0.5
            
        # Perform one-sample t-test
        t_stat, p_value = stats.ttest_1samp(values, 0)
        
        # Convert p-value to confidence score
        # Lower p-values indicate higher confidence
        significance_score = 1 - min(p_value, 1.0)
        
        # Adjust for sample size
        sample_size_factor = min(len(values) / self.min_sample_size, 1.0)
        significance_score *= sample_size_factor
        
        return significance_score

    def _assess_sample_size(self, data: Dict[str, Any]) -> float:
        """Assess adequacy of sample size."""
        values = data.get('values', [])
        if not values:
            return 0.0
            
        # Calculate score based on sample size relative to minimum
        sample_size_score = len(values) / self.min_sample_size
        return min(sample_size_score, 1.0)

    def _assess_time_relevance(self, data: Dict[str, Any]) -> float:
        """Assess time relevance of the data."""
        if 'timestamp' not in data:
            return 0.5  # Neutral score if no timestamp
            
        # Implementation would compare timestamp to current time
        # and apply decay factor based on age of data
        return 1.0  # Placeholder implementation

    def _calculate_uncertainty(self, factors: Dict[str, float]) -> float:
        """Calculate overall uncertainty measure."""
        # Higher variance in factor scores indicates higher uncertainty
        factor_values = list(factors.values())
        if not factor_values:
            return 1.0
            
        uncertainty = np.std(factor_values)
        return min(uncertainty, 1.0)

    def _calculate_reliability(self, factors: Dict[str, float]) -> float:
        """Calculate overall reliability score."""
        # Reliability is the geometric mean of data quality and consistency
        reliability = np.sqrt(factors['data_quality'] * factors['consistency'])
        return reliability

    def get_confidence_level(self, score: float) -> str:
        """Convert numerical confidence score to qualitative level.

        Args:
            score: Confidence score (0-1)

        Returns:
            Qualitative confidence level
        """
        if score >= 0.9:
            return 'Very High'
        elif score >= 0.7:
            return 'High'
        elif score >= 0.5:
            return 'Moderate'
        elif score >= 0.3:
            return 'Low'
        else:
            return 'Very Low'
