
STYLE_PROMPTS = {
    "Modern Minimalist": (
        "modern minimalist garden, geometric landscaping, "
        "clean stone pathways, manicured lawn and elegant plants"
    ),

    "Tropical Paradise": (
        "lush tropical garden, palm trees, exotic plants, "
        "vibrant greenery and natural stone pathways"
    ),

    "Japanese Zen": (
        "Japanese zen garden, carefully arranged rocks, "
        "Japanese maple trees and peaceful gravel patterns"
    ),

    "Mediterranean": (
        "Mediterranean garden, terracotta pots, olive trees, "
        "warm stone paving and lavender"
    ),

    "Luxury Contemporary": (
        "luxury contemporary garden, premium outdoor furniture, "
        "elegant lighting and sophisticated planting"
    ),

    "Natural Cottage": (
        "English cottage garden, colorful flowers, curved "
        "pathways, lush shrubs and natural planting"
    )
}


def build_prompt(analysis, style, custom_prompt=""):

    style_description = STYLE_PROMPTS.get(
        style,
        STYLE_PROMPTS["Modern Minimalist"]
    )

    prompt = f"""
    Create a photorealistic professional landscape
    architecture visualization.

    ORIGINAL SKETCH ANALYSIS:
    {analysis}

    SELECTED LANDSCAPE STYLE:
    {style_description}

    ADDITIONAL USER INSTRUCTIONS:
    {custom_prompt}

    REQUIREMENTS:
    - Preserve the original garden boundaries.
    - Maintain the original spatial arrangement.
    - Preserve existing pathways and structures.
    - Use realistic plants and natural materials.
    - Apply realistic daylight and shadows.
    - Create professional architectural photography.
    - Avoid changing the fundamental garden layout.
    """

    return prompt
