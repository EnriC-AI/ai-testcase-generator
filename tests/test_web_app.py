from web_app import DEFAULT_SPEC, render_page


def test_render_page_contains_local_web_app_form():
    html = render_page()
    assert "AI Test Case Generator" in html
    assert "Generate pytest" in html
    assert DEFAULT_SPEC.splitlines()[0].replace('"', '&quot;') in html
