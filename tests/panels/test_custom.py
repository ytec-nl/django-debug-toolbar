from django.test import override_settings

from debug_toolbar.panels import Panel

from ..base import IntegrationTestCase


class CustomPanel(Panel):
    def title(self):
        return "Title with special chars &\"'<>"


@override_settings(
    DEBUG=True, DEBUG_TOOLBAR_PANELS=["tests.panels.test_custom.CustomPanel"]
)
class CustomPanelTestCase(IntegrationTestCase):
    def test_escapes_panel_title(self):
        response = self.client.get("/regular/basic/")
        self.assertContains(
            response,
            """
            <li id="djdt-CustomPanel" class="djDebugPanelButton">
            <input type="checkbox" checked title="Disable for next and successive requests" data-cookie="djdtCustomPanel">
            <a class="CustomPanel" href="#" title="Title with special chars &amp;&quot;&#39;&lt;&gt;">
            Title with special chars &amp;&quot;&#39;&lt;&gt;
            </a>
            </li>
            """,
            html=True,
        )
        self.assertContains(
            response,
            """
            <div id="CustomPanel" class="djdt-panelContent">
            <div class="djDebugPanelTitle">
            <a href="" class="djDebugClose">×</a>
            <h3>Title with special chars &amp;&quot;&#39;&lt;&gt;</h3>
            </div>
            <div class="djDebugPanelContent">
            <img class="djdt-loader" src="/static/debug_toolbar/img/ajax-loader.gif" alt="loading">
            <div class="djdt-scroll"></div>
            </div>
            </div>
            """,
            html=True,
        )
