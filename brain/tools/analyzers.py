from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest

@dataclass
class Risk:
    """Represents a specific risk with its details."""
    name: str
    probability: float  # 0-1 scale
    impact: float      # 0-1 scale
    description: str
    mitigation_steps: List[str]

    @property
    def risk_score(self) -> float:
        """Calculate overall risk score."""
        return self.probability * self.impact

class RiskEvaluator:
    """Evaluates risks and benefits of scenarios with detailed metrics."""
    
    def __init__(self):
        self.risk_categories = [
            'technical', 'operational', 'strategic',
            'financial', 'compliance'
        ]
        self.risk_thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.3,
            'low': 0.0
        }

    def evaluate_risk(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate risks and benefits of a scenario.
        
        Args:
            scenario: Dictionary containing:
                - description: Scenario description
                - context: Additional context
                - constraints: Known limitations/requirements
                - resources: Available resources
            
        Returns:
            dict: Detailed risk assessment including:
                - risk_level: Overall risk level (low/medium/high/critical)
                - specific_risks: List of Risk objects
                - risk_matrix: Risk distribution matrix
                - benefits: List of potential benefits with impact scores
                - recommendations: Prioritized risk mitigation suggestions
                - confidence_score: Confidence in the assessment (0-1)
        """
        risks = self._identify_specific_risks(scenario)
        benefits = self._analyze_benefits(scenario)
        matrix = self._generate_risk_matrix(risks)
        confidence = self._calculate_confidence(risks, scenario)

        return {
            'risk_level': self._calculate_risk_level(risks),
            'specific_risks': risks,
            'risk_matrix': matrix,
            'benefits': benefits,
            'recommendations': self._generate_recommendations(risks, benefits),
            'confidence_score': confidence
        }

    def _identify_specific_risks(self, scenario: Dict[str, Any]) -> List[Risk]:
        """Identify specific risks based on scenario details."""
        risks = []
        for category in self.risk_categories:
            if category_risks := self._analyze_category_risks(category, scenario):
                risks.extend(category_risks)
        return risks

    def _analyze_category_risks(self, category: str, scenario: Dict[str, Any]) -> List[Risk]:
        """Analyze risks for a specific category."""
        risks = []
        # Implementation would identify category-specific risks
        # This is a placeholder for the structure
        return risks

    def _calculate_risk_level(self, risks: List[Risk]) -> str:
        """Calculate overall risk level based on specific risks."""
        if not risks:
            return 'low'
            
        max_score = max(risk.risk_score for risk in risks)
        for level, threshold in self.risk_thresholds.items():
            if max_score > threshold:
                return level
        return 'low'

    def _generate_risk_matrix(self, risks: List[Risk]) -> Dict[str, Any]:
        """Generate a risk probability/impact matrix."""
        probabilities = [risk.probability for risk in risks]
        impacts = [risk.impact for risk in risks]
        
        matrix = np.zeros((5, 5))
        if risks:
            for p, i in zip(probabilities, impacts):
                p_idx = min(int(p * 5), 4)
                i_idx = min(int(i * 5), 4)
                matrix[p_idx][i_idx] += 1

        return {
            'probability_axis': [0.2, 0.4, 0.6, 0.8, 1.0],
            'impact_axis': [0.2, 0.4, 0.6, 0.8, 1.0],
            'risk_scores': matrix.tolist()
        }

class PatternAnalyzer:
    """Identifies and analyzes patterns in data with statistical measures."""

    def __init__(self):
        self.min_correlation_strength = 0.3
        self.anomaly_threshold = 2.0  # Standard deviations
        self.anomaly_detector = IsolationForest(random_state=42)

    def find_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify patterns in data using statistical analysis.
        
        Args:
            data: Dictionary containing:
                - time_series: Optional time series data
                - categorical: Optional categorical data
                - numerical: Optional numerical data
                - metadata: Additional context
            
        Returns:
            dict: Comprehensive pattern analysis including:
                - patterns: List of identified patterns with confidence scores
                - correlations: Matrix of correlation coefficients
                - anomalies: List of detected anomalies with explanations
                - trends: Identified trends with statistical significance
                - seasonal_patterns: Any detected seasonality
                - predictions: Future predictions with confidence intervals
        """
        patterns = self._detect_patterns(data)
        correlations = self._calculate_correlations(data)
        anomalies = self._detect_anomalies(data)
        trends = self._analyze_trends(data)
        seasonality = self._find_seasonality(data)
        predictions = self._make_predictions(data)

        return {
            'patterns': patterns,
            'correlations': correlations,
            'anomalies': anomalies,
            'trends': trends,
            'seasonal_patterns': seasonality,
            'predictions': predictions
        }

    def _detect_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect significant patterns in the data."""
        patterns = []
        if 'numerical' in data:
            # Statistical pattern detection
            for var_name, values in data['numerical'].items():
                if len(values) < 2:
                    continue
                    
                # Basic statistical analysis
                stats_info = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'skew': stats.skew(values),
                    'kurtosis': stats.kurtosis(values)
                }
                
                # Detect repeating patterns
                if len(values) > 10:
                    autocorr = np.correlate(values, values, mode='full')
                    peaks = self._find_peaks(autocorr)
                    if peaks:
                        patterns.append({
                            'type': 'repeating_pattern',
                            'variable': var_name,
                            'period': peaks[0],
                            'confidence': self._calculate_pattern_confidence(peaks)
                        })
                        
                patterns.append({
                    'type': 'distribution_pattern',
                    'variable': var_name,
                    'stats': stats_info,
                    'confidence': 1.0
                })
                
        return patterns

    def _calculate_correlations(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate correlation coefficients between variables."""
        correlations = {}
        if 'numerical' in data:
            variables = list(data['numerical'].keys())
            n = len(variables)
            
            for i in range(n):
                for j in range(i + 1, n):
                    var1, var2 = variables[i], variables[j]
                    values1 = data['numerical'][var1]
                    values2 = data['numerical'][var2]
                    
                    if len(values1) == len(values2):
                        corr = np.corrcoef(values1, values2)[0, 1]
                        if abs(corr) > self.min_correlation_strength:
                            correlations[f'{var1}__{var2}'] = float(corr)
        
        return correlations

    def _detect_anomalies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect and explain anomalies in the data."""
        anomalies = []
        if 'numerical' in data:
            for var_name, values in data['numerical'].items():
                if len(values) < 2:
                    continue
                    
                # Statistical anomaly detection
                mean = np.mean(values)
                std = np.std(values)
                z_scores = np.abs((values - mean) / std)
                
                # Find statistical outliers
                outliers = np.where(z_scores > self.anomaly_threshold)[0]
                
                # Isolation Forest anomaly detection
                if len(values) > 10:
                    X = np.array(values).reshape(-1, 1)
                    self.anomaly_detector.fit(X)
                    predictions = self.anomaly_detector.predict(X)
                    isolation_outliers = np.where(predictions == -1)[0]
                    
                    # Combine both methods
                    outliers = np.unique(np.concatenate([outliers, isolation_outliers]))
                
                for idx in outliers:
                    anomalies.append({
                        'variable': var_name,
                        'index': int(idx),
                        'value': float(values[idx]),
                        'z_score': float(z_scores[idx]),
                        'confidence': float(min(1.0, z_scores[idx] / self.anomaly_threshold))
                    })
                    
        return anomalies

    def _analyze_trends(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze trends and their statistical significance."""
        trends = []
        if 'time_series' in data:
            for var_name, series in data['time_series'].items():
                if len(series) < 2:
                    continue
                    
                # Linear trend analysis
                x = np.arange(len(series))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, series)
                
                trends.append({
                    'variable': var_name,
                    'slope': float(slope),
                    'r_squared': float(r_value ** 2),
                    'p_value': float(p_value),
                    'significant': p_value < 0.05,
                    'direction': 'increasing' if slope > 0 else 'decreasing',
                    'confidence': float(1 - p_value)
                })
                
        return trends

    def _find_peaks(self, signal: np.ndarray) -> List[int]:
        """Find peaks in a signal (for pattern detection)."""
        # Simple peak detection
        peaks = []
        for i in range(1, len(signal) - 1):
            if signal[i - 1] < signal[i] > signal[i + 1]:
                peaks.append(i)
        return peaks

    def _calculate_pattern_confidence(self, peaks: List[int]) -> float:
        """Calculate confidence score for detected patterns."""
        if not peaks:
            return 0.0
        # Simple confidence based on number and regularity of peaks
        peak_diffs = np.diff(peaks)
        regularity = 1 - np.std(peak_diffs) / np.mean(peak_diffs) if len(peak_diffs) > 0 else 0
        return min(1.0, len(peaks) * regularity / 10)
