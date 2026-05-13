import flet as ft

# Color Palette
PRIMARY = "#6366f1"  # Indigo
SECONDARY = "#4f46e5"
BACKGROUND = "#0f172a"  # Slate 900
SURFACE = "#1e293b"    # Slate 800
TEXT_PRIMARY = "#f8fafc"
TEXT_SECONDARY = "#94a3b8"
ACCENT = "#10b981"     # Emerald

# Theme Configuration
THEME = ft.Theme(
    color_scheme_seed=PRIMARY,
    visual_density=ft.VisualDensity.COMFORTABLE,
)

# Shared Component Styles
CARD_STYLE = {
    "bgcolor": SURFACE,
    "padding": 20,
    "border_radius": 12,
    "shadow": ft.BoxShadow(
        blur_radius=10,
        color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
        offset=ft.Offset(0, 4),
    ),
}

INPUT_STYLE = {
    "border_color": ft.colors.with_opacity(0.2, TEXT_SECONDARY),
    "focused_border_color": PRIMARY,
    "label_style": ft.TextStyle(color=TEXT_SECONDARY),
    "color": TEXT_PRIMARY,
    "cursor_color": PRIMARY,
}

BUTTON_STYLE = ft.ButtonStyle(
    color=TEXT_PRIMARY,
    bgcolor={"": PRIMARY, "hovered": SECONDARY},
    shape=ft.RoundedRectangleBorder(radius=8),
)
