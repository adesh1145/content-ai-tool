from __future__ import annotations


class FABFrameworkService:
    """
    Domain service that builds the F-A-B (Feature-Advantage-Benefit)
    prompt structure for product descriptions.

    F-A-B breaks each product feature into:
    - Feature: What the product has
    - Advantage: Why it's better than alternatives
    - Benefit: How it helps the customer
    """

    @staticmethod
    def build_fab_prompt(
        product_name: str,
        category: str,
        features: list[str],
        tone: str,
        target_audience: str,
        word_count: int,
    ) -> str:
        features_block = "\n".join(f"- {f}" for f in features)
        return (
            f"Product: {product_name}\n"
            f"Category: {category}\n"
            f"Features:\n{features_block}\n\n"
            "Using the F-A-B (Feature-Advantage-Benefit) framework, "
            "for each feature above, identify:\n"
            "1. The Feature itself\n"
            "2. The Advantage it provides over alternatives\n"
            "3. The concrete Benefit to the customer\n\n"
            "Then weave all F-A-B points into a compelling, cohesive product description.\n"
            f"Target audience: {target_audience}\n"
            f"Tone: {tone}\n"
            f"Target word count: {word_count}\n\n"
            "Return ONLY the final product description text, nothing else."
        )
