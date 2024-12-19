from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import numpy as np
from scipy import stats
from .base import BaseTool

@dataclass
class ConfidenceScore:
    """Represents a confidence assessment with detailed metrics."""
    score: float  # Overall confidence score (0-1)
    factors: Dict[str, float]  # Individual factor scores
    uncertainty: float  # Uncertainty measure (0-1)
    reliability: float  # Data reliability score (0-1)
    sample_size: int  # Number of data points considered

def evaluate_confidence(data: Dict[str, Any], min_sample_size: int = 5) -> ConfidenceScore:
    """Evaluate confidence level based on provided data.

    Args:
        data: Dictionary containing:
            - values: List of numerical values or observations
            - metadata: Additional context and quality indicators
            - timestamp: Optional timestamp for time relevance
        min_sample_size: Minimum sample size for full confidence

    Returns:
        ConfidenceScore object with detailed metrics
    """
    weight_factors = {
        'data_quality': 0.3,
        'consistency': 0.2,
        'statistical_significance': 0.2,
        'sample_size': 0.15,
        'time_relevance': 0.15
    }
    
    factors = {}
    
    # Assess data quality
    values = data.get('values', [])
    metadata = data.get('metadata', {})
    
    if not values:
        factors['data_quality'] = 0.0
    else:
        missing_ratio = sum(1 for v in values if v is None) / len(values)
        quality_score = (1 - missing_ratio)
        if metadata.get('validation_errors', []):
            quality_score *= 0.7
        source_reliability = metadata.get('source_reliability', 1.0)
        factors['data_quality'] = quality_score * source_reliability
    
    # Assess consistency
    if not values or len(values) < 2:
        factors['consistency'] = 0.5
    else:
        values_array = np.array([v for v in values if v is not None])
        cv = np.std(values_array) / np.mean(values_array) if np.mean(values_array) != 0 else 1.0
        consistency_score = 1 / (1 + cv)
        z_scores = np.abs(stats.zscore(values_array))
        outlier_ratio = np.sum(z_scores > 3) / len(values_array)
        factors['consistency'] = consistency_score * (1 - outlier_ratio)
    
    # Assess statistical significance
    if not values or len(values) < 2:
        factors['statistical_significance'] = 0.5
    else:
        values_array = np.array([v for v in values if v is not None])
        _, p_value = stats.ttest_1samp(values_array, 0)
        significance_score = 1 - min(p_value, 1.0)
        sample_size_factor = min(len(values_array) / min_sample_size, 1.0)
        factors['statistical_significance'] = significance_score * sample_size_factor
    
    # Assess sample size
    factors['sample_size'] = min(len(values) / min_sample_size, 1.0) if values else 0.0
    
    # Assess time relevance
    factors['time_relevance'] = 1.0 if 'timestamp' in data else 0.5
    
    # Calculate overall confidence score
    overall_score = sum(score * weight_factors[factor]
                       for factor, score in factors.items())
    
    # Calculate uncertainty
    uncertainty = min(np.std(list(factors.values())), 1.0) if factors else 1.0
    
    # Calculate reliability
    reliability = np.sqrt(factors['data_quality'] * factors['consistency'])
    
    return ConfidenceScore(
        score=overall_score,
        factors=factors,
        uncertainty=uncertainty,
        reliability=reliability,
        sample_size=len(values)
    )

def get_confidence_level(score: float) -> str:
    """Convert numerical confidence score to qualitative level.

    Args:
        score: Confidence score (0-1)

    Returns:
        str: Qualitative confidence level
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

# Create tool instances
confidence_evaluator = BaseTool(
    name="confidence_evaluator",
    func=evaluate_confidence,
    description="Evaluates confidence levels in data with detailed metrics and uncertainty analysis."
)

confidence_level = BaseTool(
    name="confidence_level",
    func=get_confidence_level,
    description="Converts numerical confidence scores to qualitative confidence levels."
)