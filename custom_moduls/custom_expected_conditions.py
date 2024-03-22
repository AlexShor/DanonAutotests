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


def element_has_css_class(method, css_selector, class_name):
    def _predicate(browser):

        element = browser.find_element(method, css_selector)

        if class_name in element.get_attribute("class"):
            return True
        else:
            return False

    return _predicate
