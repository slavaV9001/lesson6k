import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture
def driver():
    driver = webdriver.Edge(
        service=EdgeService(
            EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


def test_form(driver):
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        )
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.NAME, 'first-name')))

    driver.find_element(By.NAME, "first-name").send_keys("Иван")
    driver.find_element(By.NAME, "last-name").send_keys("Петров")
    driver.find_element(By.NAME, "address").send_keys("Ленина, 55-3")
    driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com")
    driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
    driver.find_element(By.NAME, "zip-code").send_keys("")
    driver.find_element(By.NAME, "city").send_keys("Москва")
    driver.find_element(By.NAME, "country").send_keys("Россия")
    driver.find_element(By.NAME, "job-position").send_keys("QA")
    driver.find_element(By.NAME, "company").send_keys("SkyPro")

    driver.find_element(By.ID, "submit").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.CLASS_NAME, "form-group"))
            )

    zip_code_field = driver.find_element(By.ID, "zip-code")

    assert "border-color: red" in zip_code_field.get_attribute
    ("style"), "Zip code field is not highlighted in red."

    fields = [
        "first-name",
        "last-name",
        "address",
        "e-mail",
        "phone",
        "city",
        "country",
        "job-position",
        "company"
    ]

    for field_name in fields:
        field = driver.find_element(By.ID, field_name)
        assert "border-color: green" in field.get_attribute(
            "style"), f"{field_name} field is not highlighted in green."

    driver.quit()


print("успех")
