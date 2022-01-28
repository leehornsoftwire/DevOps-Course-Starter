from behave import given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By


def goto_page(context, relative_url: str):
    context.driver.get(f"http:/localhost:5000/{relative_url}")


@given("I use the Trello backend")
def step_impl(context):
    driver: webdriver.Firefox = context.driver
    context.execute_steps(
        """When I go to the home page
    and I click the "Switch backend" button
    """
    )


@when("I go to the home page")
def step_impl(context):
    goto_page(context, "")


@when('I click the "{text}" button')
def step_impl(context, text):
    driver: webdriver.Firefox = context.driver
    button = driver.find_element(By.CSS_SELECTOR, f'input[value="{text}"]')
    button.click()


@when('I type "{text}" into the "{box_id}" box')
def step_impl(context, text, box_id):
    driver: webdriver.Firefox = context.driver
    box = driver.find_element(By.CSS_SELECTOR, f'input[id="{box_id}"]')
    box.send_keys(text)


@then('I should see "{text}"')
def step_impl(context, text):
    print(context.driver.page_source)
    assert text in context.driver.page_source


@then('I should not see "{text}"')
def step_impl(context, text):
    print(context.driver.page_source)
    assert text not in context.driver.page_source
