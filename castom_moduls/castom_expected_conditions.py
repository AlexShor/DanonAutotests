def element_has_scroll_size(locator, expected_scroll_height):
    def _predicate(browser):

        scroll_height = browser.execute_script(
            f'''return document.evaluate(
                '{locator}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
            ).singleNodeValue.scrollHeight''')

        if scroll_height >= expected_scroll_height:
            return True
        else:
            return False

    return _predicate
