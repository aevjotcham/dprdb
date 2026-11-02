"""Sphinx and Shibuya configuration for the DPRDB league archive."""

project = "DaBois Fantasy League Archives"
extensions = ["myst_parser", "sphinx.ext.githubpages"]
root_doc = "index"
html_theme = "shibuya"
html_title = project
html_static_path = ["_static"]
html_css_files = ["archive.css"]
html_js_files = ["league-selector.js"]
templates_path = ["_templates"]
html_show_sourcelink = False
html_copy_source = False
html_use_index = False
html_show_copyright = False
html_theme_options = {
    "page_layout": "default",
    "accent_color": "cyan",
    "color_mode": "light",
    "toctree_includehidden": False,
    "globaltoc_expand_depth": 1,
}

html_context = {'leagues': [{'slug': 'dba', 'name': 'DaBois Basketball Association'},
             {'slug': 'dfl', 'name': 'DaBois Football League'},
             {'slug': 'dlb', 'name': 'DaBois League Baseball'}],
 'league_sections': [('managers', 'Managers'),
                     ('standings', 'Standings'),
                     ('news', 'News'),
                     ('championship-history', 'Championship History'),
                     ('franchise-history', 'Franchise History'),
                     ('season-history', 'Season History'),
                     ('playoff-history', 'Playoff History'),
                     ('awards', 'Awards')]}
