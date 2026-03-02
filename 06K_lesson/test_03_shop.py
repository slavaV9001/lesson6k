from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def driver():
    driver = webdriver.Firefox(
        service=FirefoxService(
            GeckoDriverManager().install())
            )
    driver.maximize_window()
    yield driver
    driver.quit()


def test_saucedemo_total_price(driver):
    wait = WebDriverWait(driver, 45)
    # переход на страницу
    driver.get('https://www.saucedemo.com/')

    # авторизация
    wait.until(
        EC.presence_of_element_located((
            By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # добавление товаров
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ]
    for item_name in items_to_add:
        xpath = (
            "//div[contains(@class, 'inventory_item_name') "
            f"and contains(., '{item_name}')]"
            "/following::button[contains(@class, 'btn_inventory')]"
            )

        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        add_button.click()

    # переходим в корзину
    wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, ".shopping_cart_link"))).click()
    wait.until(EC.visibility_of_element_located((
        By.CLASS_NAME, "cart_list")))

    wait.until(EC.element_to_be_clickable((By.ID, 'checkout'))).click()

    # заполняем данные
    wait.until(EC.presence_of_element_located((
        By.ID, "first-name"))).send_keys("Вячеслав")
    driver.find_element(By.ID, "last-name").send_keys("Величко")
    driver.find_element(By.ID, "postal-code").send_keys("505055")
    driver.find_element(By.ID, "continue").click()
    # итоговая сумма
    total_element = wait.until(
        EC.visibility_of_element_located((
            By.CLASS_NAME, "summary_total_label")))
    total_text = total_element.text

    assert 'Total: $58.29' in total_text, f"Ожидали $58.29, а получили '{
        total_text}'"
    print("Успех")
    driver.quit()


print("Final")
