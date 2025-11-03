"""
LLM Analysis Module for Healthcare Facility Planning

This module provides Large Language Model integration for generating
policy recommendations and insights based on accessibility data.

Supports:
- OpenAI GPT-3.5/GPT-4 (via API)
- Hugging Face models (local or API)

Author: Healthcare Facility Planning Team
Date: 2025-11-03
"""

import os
import json
from typing import Dict, List, Optional, Union
from datetime import datetime


class LLMAnalyzer:
    """
    Large Language Model analyzer for healthcare accessibility insights.

    Supports multiple LLM providers:
    - OpenAI (GPT-3.5-turbo, GPT-4)
    - Hugging Face (microsoft/phi-2, etc.)
    """

    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize LLM Analyzer.

        Args:
            provider: 'openai', 'huggingface', or 'local' (default from env)
            model: Model name (default from env)
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        self.model = model or self._get_default_model()
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', 500))
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.7))

        # Initialize provider-specific client
        if self.provider == 'openai':
            self._init_openai()
        elif self.provider == 'huggingface':
            self._init_huggingface()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _get_default_model(self) -> str:
        """Get default model based on provider"""
        defaults = {
            'openai': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            'huggingface': os.getenv('HUGGINGFACE_MODEL', 'microsoft/phi-2')
        }
        return defaults.get(self.provider, 'gpt-3.5-turbo')

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            self.client = openai
            self.client.api_key = os.getenv('OPENAI_API_KEY')

            if not self.client.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")

            print(f"✅ OpenAI client initialized with model: {self.model}")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def _init_huggingface(self):
        """Initialize Hugging Face client"""
        try:
            from transformers import pipeline
            import torch

            device = 0 if torch.cuda.is_available() else -1
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                device=device
            )
            print(f"✅ Hugging Face pipeline initialized with model: {self.model}")
        except ImportError:
            raise ImportError("transformers package not installed. Run: pip install transformers torch")

    def analyze_accessibility(
        self,
        accessibility_data: Dict,
        underserved_districts: List[Dict],
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze healthcare accessibility data and generate insights.

        Args:
            accessibility_data: Dict with keys:
                - total_districts: int
                - underserved_count: int
                - average_accessibility: float
                - coverage_pct: float
                - avg_travel_time: float
            underserved_districts: List of dicts with keys:
                - district: str
                - accessibility_score: float
                - avg_travel_time: float
                - population: int
            context: Optional additional context

        Returns:
            Dict with LLM analysis including:
                - insights: str (key findings)
                - recommendations: List[str]
                - priority_areas: List[Dict]
                - strategic_actions: List[str]
                - hssp_alignment: Dict
        """
        prompt = self._build_prompt(accessibility_data, underserved_districts, context)

        start_time = datetime.now()

        if self.provider == 'openai':
            response = self._call_openai(prompt)
        elif self.provider == 'huggingface':
            response = self._call_huggingface(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        # Parse and structure the response
        structured_response = self._parse_llm_response(response)

        return {
            **structured_response,
            'metadata': {
                'model': self.model,
                'provider': self.provider,
                'processing_time_ms': int(processing_time),
                'generated_at': datetime.now().isoformat()
            }
        }

    def _build_prompt(
        self,
        accessibility_data: Dict,
        underserved_districts: List[Dict],
        context: Optional[Dict]
    ) -> str:
        """Build structured prompt for LLM"""

        # HSSP V targets
        hssp_target_travel_time = int(os.getenv('HSSP_TARGET_TRAVEL_TIME', 25))
        hssp_target_coverage = int(os.getenv('HSSP_TARGET_COVERAGE', 95))

        prompt = f"""You are a healthcare policy analyst for Rwanda's Ministry of Health, specializing in healthcare facility planning and the Health Sector Strategic Plan V (HSSP V).

# Context
Rwanda aims to achieve Universal Health Coverage (UHC) by 2030. The HSSP V sets specific targets:
- WHO Target: Maximum 25 minutes travel time to nearest healthcare facility
- Population coverage target: {hssp_target_coverage}% of population within 25-minute access
- Facility density target: 5 facilities per 10,000 people

# Current Accessibility Data
- Total districts analyzed: {accessibility_data.get('total_districts', 'N/A')}
- Underserved districts: {accessibility_data.get('underserved_count', 'N/A')}
- National average accessibility score: {accessibility_data.get('average_accessibility', 'N/A'):.3f} (0-1 scale)
- Population coverage: {accessibility_data.get('coverage_pct', 'N/A')}%
- Average travel time: {accessibility_data.get('avg_travel_time', 'N/A')} minutes

# Top 3 Most Underserved Districts
"""

        for i, district in enumerate(underserved_districts[:3], 1):
            prompt += f"""
{i}. {district.get('district', 'Unknown')}
   - Accessibility score: {district.get('accessibility_score', 0):.3f}
   - Avg travel time: {district.get('avg_travel_time', 'N/A')} minutes
   - Population: {district.get('population', 'N/A'):,}
   - Existing facilities: {district.get('facility_count', 'N/A')}
"""

        if context:
            prompt += f"\n# Additional Context\n{json.dumps(context, indent=2)}\n"

        prompt += f"""

# Your Task
Based on the above data, provide a comprehensive analysis with:

1. **Key Insights** (3-5 bullet points)
   - What are the most critical accessibility challenges?
   - Which districts require urgent attention?
   - What patterns do you observe?

2. **Immediate Recommendations** (Top 3 priority actions)
   - Specific, actionable steps for the next 3-6 months
   - Focus on high-impact, feasible interventions

3. **Strategic Planning** (Long-term actions)
   - 5-year infrastructure development strategy
   - Telemedicine and technology solutions
   - Transportation infrastructure improvements

4. **Resource Allocation**
   - How to prioritize funding across districts
   - Healthcare worker deployment strategy
   - Equipment and supply chain recommendations

5. **HSSP V Alignment**
   - Gap analysis vs. WHO 25-minute target
   - Estimated timeline to reach targets
   - Risk factors and mitigation strategies

Format your response as structured JSON with these keys:
- insights: array of strings
- immediate_recommendations: array of objects with 'action', 'district', 'impact', 'timeline'
- strategic_planning: array of objects with 'initiative', 'description', 'timeframe'
- resource_allocation: object with 'funding_priorities', 'workforce_strategy', 'equipment_needs'
- hssp_alignment: object with 'current_gap', 'estimated_completion', 'key_risks'

Ensure recommendations are evidence-based, culturally appropriate for Rwanda, and aligned with HSSP V goals.
"""

        return prompt

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert healthcare policy analyst specializing in Rwanda's health sector and the HSSP V strategic plan."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return self._get_fallback_response()

    def _call_huggingface(self, prompt: str) -> str:
        """Call Hugging Face pipeline"""
        try:
            response = self.pipeline(
                prompt,
                max_length=self.max_tokens,
                temperature=self.temperature,
                do_sample=True
            )

            return response[0]['generated_text']

        except Exception as e:
            print(f"❌ Hugging Face error: {e}")
            return self._get_fallback_response()

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            # LLMs sometimes wrap JSON in markdown code blocks
            if '```json' in response:
                json_str = response.split('```json')[1].split('```')[0].strip()
            elif '```' in response:
                json_str = response.split('```')[1].split('```')[0].strip()
            else:
                json_str = response.strip()

            parsed = json.loads(json_str)
            return parsed

        except (json.JSONDecodeError, IndexError):
            # If JSON parsing fails, return structured fallback
            print("⚠️ Could not parse LLM response as JSON, using text extraction")
            return self._extract_structure_from_text(response)

    def _extract_structure_from_text(self, text: str) -> Dict:
        """Extract structure from free-form text response"""
        # Basic text parsing fallback
        return {
            'insights': [text[:200]],  # First 200 chars as insight
            'immediate_recommendations': [
                {
                    'action': 'Review detailed LLM response',
                    'district': 'All underserved',
                    'impact': 'High',
                    'timeline': '3-6 months'
                }
            ],
            'strategic_planning': [
                {
                    'initiative': 'See full LLM response',
                    'description': text[200:400] if len(text) > 200 else text,
                    'timeframe': '5 years'
                }
            ],
            'resource_allocation': {
                'funding_priorities': 'Underserved districts',
                'workforce_strategy': 'Deploy to high-need areas',
                'equipment_needs': 'Based on facility type'
            },
            'hssp_alignment': {
                'current_gap': 'Analysis required',
                'estimated_completion': 'To be determined',
                'key_risks': 'Resource constraints'
            },
            'raw_response': text
        }

    def _get_fallback_response(self) -> str:
        """Generate fallback response when LLM is unavailable"""
        return json.dumps({
            'insights': [
                'LLM service temporarily unavailable',
                'Using rule-based analysis',
                'Please check API credentials and try again'
            ],
            'immediate_recommendations': [
                {
                    'action': 'Conduct field assessment in districts with >60 min travel time',
                    'district': 'All critical priority',
                    'impact': 'High',
                    'timeline': '1-3 months'
                }
            ],
            'strategic_planning': [
                {
                    'initiative': 'Healthcare infrastructure expansion',
                    'description': 'Systematic facility placement based on ML analysis',
                    'timeframe': '5 years'
                }
            ],
            'resource_allocation': {
                'funding_priorities': 'Districts below HSSP V targets',
                'workforce_strategy': 'Incentivize deployment to rural areas',
                'equipment_needs': 'Essential equipment for new facilities'
            },
            'hssp_alignment': {
                'current_gap': 'Significant - requires intervention',
                'estimated_completion': '2028-2030',
                'key_risks': 'Funding, infrastructure, workforce'
            }
        })


# Utility functions for direct use

def analyze_with_llm(
    accessibility_data: Dict,
    underserved_districts: List[Dict],
    provider: str = 'openai'
) -> Dict:
    """
    Convenience function to analyze accessibility data with LLM.

    Args:
        accessibility_data: Accessibility metrics dictionary
        underserved_districts: List of underserved district data
        provider: 'openai' or 'huggingface'

    Returns:
        Structured LLM analysis
    """
    analyzer = LLMAnalyzer(provider=provider)
    return analyzer.analyze_accessibility(accessibility_data, underserved_districts)


def get_policy_recommendations(district_name: str, metrics: Dict) -> Dict:
    """
    Get policy recommendations for a specific district.

    Args:
        district_name: Name of the district
        metrics: Accessibility metrics for the district

    Returns:
        District-specific recommendations
    """
    analyzer = LLMAnalyzer()

    accessibility_data = {
        'total_districts': 1,
        'underserved_count': 1 if metrics.get('accessibility_score', 1) < 0.7 else 0,
        'average_accessibility': metrics.get('accessibility_score', 0),
        'coverage_pct': metrics.get('population_coverage_pct', 0),
        'avg_travel_time': metrics.get('avg_travel_time_minutes', 0)
    }

    underserved_districts = [
        {
            'district': district_name,
            **metrics
        }
    ]

    return analyzer.analyze_accessibility(accessibility_data, underserved_districts)


if __name__ == '__main__':
    # Example usage
    print("🧪 Testing LLM Analyzer...")

    # Sample data
    test_data = {
        'total_districts': 5,
        'underserved_count': 3,
        'average_accessibility': 0.58,
        'coverage_pct': 68,
        'avg_travel_time': 52
    }

    test_districts = [
        {
            'district': 'Gicumbi',
            'accessibility_score': 0.35,
            'avg_travel_time': 62,
            'population': 485000,
            'facility_count': 12
        },
        {
            'district': 'Kayonza',
            'accessibility_score': 0.52,
            'avg_travel_time': 45,
            'population': 344000,
            'facility_count': 18
        }
    ]

    try:
        analyzer = LLMAnalyzer()
        result = analyzer.analyze_accessibility(test_data, test_districts)

        print("\n✅ LLM Analysis Result:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure to set environment variables:")
        print("- OPENAI_API_KEY (for OpenAI)")
        print("- Or use provider='huggingface' with transformers installed")
