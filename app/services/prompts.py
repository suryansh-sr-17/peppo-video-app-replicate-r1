import hashlib

STYLE_PRESETS = {
    "cinematic": {
        "guidance": "cinematic lighting, shallow depth of field, smooth camera dolly, 24fps film look",
        "negatives": "no watermarks, no text artifacts, avoid jitter"
    },
    "anime": {
        "guidance": "stylized anime look, dynamic motion lines, vibrant palette, cel shading",
        "negatives": "avoid photorealism, avoid noise"
    },
    "product": {
        "guidance": "clean studio lighting, 360-degree orbit, seamless background, crisp focus",
        "negatives": "no hands, no fingers, no logos"
    }
}

def compose_prompt(user_prompt: str, style: str = "cinematic") -> str:
    st = STYLE_PRESETS.get(style, {})
    g = st.get("guidance", "")
    n = st.get("negatives", "")
    return f"{user_prompt}. Style: {style}. Visual guidance: {g}. Negative prompts: {n}."

def prompt_hash(user_prompt: str, style: str) -> str:
    return hashlib.sha256(f"{user_prompt}|{style}".encode()).hexdigest()[:16]
