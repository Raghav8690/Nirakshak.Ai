"""
Nirikshak.AI — LLM Provider (Abstraction Layer)
=================================================
Provides an abstract interface for LLM calls so the provider can be swapped
via configuration. Ships with a MockLLMProvider that returns realistic
canned responses — NO API KEY OR PAID SERVICE REQUIRED.

To plug in a real provider later, implement the LLMProvider interface
and update the factory function.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import random


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_recommendation(
        self,
        customer_context: Dict[str, Any],
        signal: Dict[str, Any],
        product_context: str,
    ) -> Dict[str, Any]:
        """
        Generate a product recommendation with explanation.

        Args:
            customer_context: Customer profile and transaction summary
            signal: Detected pattern/signal from PatternDetector
            product_context: Retrieved product knowledge (from RAG)

        Returns:
            Dict with: recommendation, explanation, reasoning_trace, confidence
        """
        pass


class MockLLMProvider(LLMProvider):
    """
    Free, offline LLM provider that returns realistic mock responses.
    Used for hackathon demos — no API key needed.
    """

    # Pre-built response templates keyed by trigger type
    RESPONSE_TEMPLATES = {
        "rent_no_insurance": {
            "product": "SBI Health Insurance — Arogya Premier",
            "product_category": "Insurance",
            "explanation": (
                "You've been consistently paying rent, which shows financial discipline. "
                "However, we noticed you don't have health insurance coverage yet. "
                "A sudden medical emergency could impact your savings significantly. "
                "SBI Arogya Premier offers comprehensive coverage starting at just ₹500/month."
            ),
            "reasoning_steps": [
                "Detected consistent rent payments for 3+ months",
                "No insurance premium transactions found in history",
                "Customer age and income profile suggests insurance gap",
                "Retrieved SBI Arogya Premier as best-fit product",
                "Generated personalized explanation based on customer context",
            ],
        },
        "salary_hike": {
            "product": "SBI Mutual Fund — Equity SIP",
            "product_category": "Investment",
            "explanation": (
                "Congratulations on your salary increase! This is a great time to start "
                "investing the incremental income. A Systematic Investment Plan (SIP) in "
                "SBI Equity Mutual Fund can help you build long-term wealth with as little "
                "as ₹500/month, while keeping your current lifestyle unchanged."
            ),
            "reasoning_steps": [
                "Detected salary increase of >20% compared to historical average",
                "Customer risk profile is moderate — equity SIP is suitable",
                "No existing investment transactions detected",
                "Retrieved SBI Mutual Fund SIP as best-fit product",
                "Generated explanation emphasizing incremental income investment",
            ],
        },
        "dormant_savings": {
            "product": "SBI Fixed Deposit — Special Rate",
            "product_category": "Investment",
            "explanation": (
                "Your savings account has been idle for a while. Idle money loses value "
                "to inflation over time. Consider parking it in an SBI Fixed Deposit "
                "at a special rate of 7.1% p.a. — your money works for you while staying safe."
            ),
            "reasoning_steps": [
                "Detected no significant debits in 60+ days",
                "Account balance suggests idle savings",
                "Customer risk profile is conservative to moderate",
                "Retrieved SBI FD special rate offer as best-fit product",
                "Generated explanation focusing on inflation protection",
            ],
        },
        "emi_ending": {
            "product": "SBI Home Loan — Top-Up / Balance Transfer",
            "product_category": "Loan",
            "explanation": (
                "We noticed you have active EMI commitments. If you're looking to "
                "optimize your monthly outflow, SBI offers competitive home loan "
                "balance transfer rates starting at 8.5% p.a. — potentially saving "
                "you thousands per month."
            ),
            "reasoning_steps": [
                "Detected 3+ recurring EMI payments",
                "Calculated average EMI burden relative to income",
                "Customer may benefit from loan restructuring",
                "Retrieved SBI Home Loan top-up/balance transfer as best-fit",
                "Generated explanation highlighting potential savings",
            ],
        },
        "high_spend_category": {
            "product": "SBI Credit Card — Cashback Rewards",
            "product_category": "Card",
            "explanation": (
                "We noticed a significant portion of your spending is concentrated "
                "in one category. An SBI Cashback Credit Card could help you earn "
                "up to 5% cashback on these purchases, effectively reducing your "
                "monthly expenses."
            ),
            "reasoning_steps": [
                "Detected >40% spending concentration in a single category",
                "Category matches cashback reward eligibility",
                "Customer does not currently hold a rewards credit card",
                "Retrieved SBI Cashback Credit Card as best-fit product",
                "Generated explanation emphasizing savings potential",
            ],
        },
        "large_withdrawal": {
            "product": "SBI Personal Loan — Quick Disbursal",
            "product_category": "Loan",
            "explanation": (
                "A large withdrawal was detected from your account. If this was for "
                "an urgent need, SBI Personal Loan offers quick disbursal at competitive "
                "rates with flexible repayment terms, so you can replenish your savings."
            ),
            "reasoning_steps": [
                "Detected single withdrawal exceeding 50% of monthly income",
                "Pattern suggests potential urgent financial need",
                "Customer credit profile supports personal loan eligibility",
                "Retrieved SBI Personal Loan as best-fit product",
                "Generated explanation focusing on savings replenishment",
            ],
        },
    }

    def generate_recommendation(
        self,
        customer_context: Dict[str, Any],
        signal: Dict[str, Any],
        product_context: str,
    ) -> Dict[str, Any]:
        """Return a realistic mock recommendation."""
        trigger_type = signal.get("trigger_type", "")
        template = self.RESPONSE_TEMPLATES.get(trigger_type, {
            "product": "SBI Smart Banking Suite",
            "product_category": "Digital",
            "explanation": "Based on your recent activity, we have a personalized recommendation for you.",
            "reasoning_steps": ["Pattern detected", "Context analyzed", "Product matched"],
        })

        # Add slight confidence variation for realism
        base_confidence = signal.get("confidence", 0.7)
        confidence = min(1.0, base_confidence + random.uniform(-0.05, 0.10))

        return {
            "product_recommended": template["product"],
            "product_category": template["product_category"],
            "explanation": template["explanation"],
            "confidence": round(confidence, 2),
            "reasoning_trace": {
                "trigger_type": trigger_type,
                "signal": signal.get("signal_detected", ""),
                "steps": template["reasoning_steps"],
                "customer_context_used": list(customer_context.keys()),
                "product_knowledge_retrieved": product_context[:200] if product_context else "N/A",
                "model": "MockLLM v1.0 (Hackathon Demo)",
            },
        }


def get_llm_provider(provider_name: str = "mock") -> LLMProvider:
    """
    Factory function to get the configured LLM provider.
    Currently only 'mock' is implemented (free, no API key).
    Extend this to add real providers.
    """
    providers = {
        "mock": MockLLMProvider,
        # Future: "openai": OpenAIProvider, "claude": ClaudeProvider
    }

    provider_class = providers.get(provider_name, MockLLMProvider)
    return provider_class()
