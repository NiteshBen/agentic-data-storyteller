import html
from typing import Dict, Any, List

class InfographicGenerator:
    """
    Generates high-resolution, vector SVG infographic summary cards
    suitable for LinkedIn posts, GitHub README displays, and executive briefs.
    """

    @staticmethod
    def generate_svg(
        title: str,
        subtitle: str,
        kpis: List[Dict[str, str]],
        takeaways: List[str],
        output_path: str
    ) -> str:
        """
        Creates a clean 1200x630 (standard social card aspect ratio) SVG infographic.
        """
        escaped_title = html.escape(title)
        escaped_subtitle = html.escape(subtitle)
        
        # Build KPI Cards (up to 4)
        kpi_svg_chunks = []
        card_width = 240
        card_height = 110
        card_y = 170
        spacing = 30
        start_x = 75
        
        for idx, kpi in enumerate(kpis[:4]):
            kx = start_x + idx * (card_width + spacing)
            label = html.escape(kpi.get("label", "Metric"))
            value = html.escape(kpi.get("value", "0"))
            sub = html.escape(kpi.get("sub", ""))
            
            kpi_svg_chunks.append(f"""
            <g transform="translate({kx}, {card_y})">
                <rect width="{card_width}" height="{card_height}" rx="12" fill="#1E293B" stroke="#334155" stroke-width="1.5" />
                <text x="20" y="32" font-family="Inter, -apple-system, sans-serif" font-size="13" font-weight="600" fill="#94A3B8" letter-spacing="0.5">{label.upper()}</text>
                <text x="20" y="70" font-family="Inter, -apple-system, sans-serif" font-size="30" font-weight="700" fill="#38BDF8">{value}</text>
                <text x="20" y="94" font-family="Inter, -apple-system, sans-serif" font-size="12" fill="#64748B">{sub}</text>
            </g>
            """)

        # Build Takeaways
        takeaway_svg_chunks = []
        t_y = 330
        for i, text in enumerate(takeaways[:3]):
            escaped_text = html.escape(text)
            curr_y = t_y + (i * 75)
            takeaway_svg_chunks.append(f"""
            <g transform="translate(75, {curr_y})">
                <rect width="1050" height="60" rx="8" fill="#131D31" stroke="#223049" stroke-width="1" />
                <circle cx="28" cy="30" r="14" fill="#0284C7" fill-opacity="0.2" />
                <text x="28" y="35" text-anchor="middle" font-family="Inter, sans-serif" font-size="14" font-weight="700" fill="#38BDF8">{i+1}</text>
                <text x="56" y="36" font-family="Inter, -apple-system, sans-serif" font-size="16" fill="#E2E8F0" font-weight="500">{escaped_text}</text>
            </g>
            """)

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
    <defs>
        <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#0B0F19" />
            <stop offset="50%" stop-color="#0F172A" />
            <stop offset="100%" stop-color="#090D16" />
        </linearGradient>
        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#38BDF8" />
            <stop offset="100%" stop-color="#818CF8" />
        </linearGradient>
    </defs>

    <!-- Background -->
    <rect width="1200" height="630" fill="url(#bgGradient)" />

    <!-- Top Accent Bar -->
    <rect x="0" y="0" width="1200" height="6" fill="url(#accentGrad)" />

    <!-- Header Section -->
    <g transform="translate(75, 60)">
        <rect x="0" y="0" width="140" height="26" rx="6" fill="#1E293B" />
        <text x="70" y="17" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#38BDF8" letter-spacing="1">AGENTIC INSIGHTS</text>
        <text x="0" y="58" font-family="Inter, -apple-system, sans-serif" font-size="34" font-weight="800" fill="#FFFFFF">{escaped_title}</text>
        <text x="0" y="85" font-family="Inter, -apple-system, sans-serif" font-size="16" font-weight="400" fill="#94A3B8">{escaped_subtitle}</text>
    </g>

    <!-- KPI Cards -->
    {''.join(kpi_svg_chunks)}

    <!-- Takeaways Section Header -->
    <text x="75" y="315" font-family="Inter, -apple-system, sans-serif" font-size="13" font-weight="700" fill="#64748B" letter-spacing="1">CORE DISCOVERIES &amp; EXECUTIVE TAKEAWAYS</text>

    <!-- Takeaways List -->
    {''.join(takeaway_svg_chunks)}

    <!-- Footer Branding -->
    <g transform="translate(75, 590)">
        <text x="0" y="0" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#475569">Engineered by <tspan fill="#38BDF8" font-weight="600">Nitesh Beniwal</tspan> | Agentic Data Storyteller</text>
        <text x="1050" y="0" text-anchor="end" font-family="Inter, sans-serif" font-size="13" fill="#475569">Autonomous Multi-Agent Intelligence</text>
    </g>
</svg>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
            
        return output_path
