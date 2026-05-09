import unittest

from airi.router import Intent, clean_remember_text, route_message


class TestRouter(unittest.TestCase):
    def test_clean_remember_text_removes_zapomni_chto(self):
        result = clean_remember_text("запомни что меня зовут Ильяс")
        self.assertEqual(result, "меня зовут Ильяс")

    def test_clean_remember_text_with_colon(self):
        result = clean_remember_text("запомни: Саша любит черный юмор")
        self.assertEqual(result, "Саша любит черный юмор")

    def test_route_remember(self):
        route = route_message("запомни что я учу ML")

        self.assertEqual(route.intent, Intent.REMEMBER)
        self.assertEqual(route.content, "я учу ML")

    def test_route_show_memory_command(self):
        route = route_message("/memory")

        self.assertEqual(route.intent, Intent.SHOW_MEMORY)

    def test_route_show_memory_question(self):
        route = route_message("что ты помнишь?")

        self.assertEqual(route.intent, Intent.SHOW_MEMORY)

    def test_route_clear_history(self):
        route = route_message("/clear")

        self.assertEqual(route.intent, Intent.CLEAR_HISTORY)

    def test_route_chat(self):
        route = route_message("объясни что такое нейросеть")

        self.assertEqual(route.intent, Intent.CHAT)
        self.assertEqual(route.content, "объясни что такое нейросеть")

    def test_route_search_memory(self):
        route = route_message("/search Саша")

        self.assertEqual(route.intent, Intent.SEARCH_MEMORY)
        self.assertEqual(route.content, "Саша")

    def test_route_forget_memory(self):
        route = route_message("/forget 3")

        self.assertEqual(route.intent, Intent.FORGET_MEMORY)
        self.assertEqual(route.content, "3")


if __name__ == "__main__":
    unittest.main()