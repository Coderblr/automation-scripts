/*
 * Auto-generated test script from Excel
 * Test Case: TC011 - Product Details Navigation
 * Generated: 2026-03-21 11:02:04
 */

package com.automation.tests;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.time.Duration;

public class TestProductDetailsNavigation {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeMethod
    public void setUp() {
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--no-sandbox", "--disable-dev-shm-usage");
        driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
    }

    @Test(description = "Product Details Navigation")
    public void test_product_details_navigation() throws Exception {
        // Step 1: navigate
        driver.get("https://www.saucedemo.com/v1/");

        // Step 2: type
        WebElement el2 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("user-name")));
        el2.clear();
        el2.sendKeys("standard_user");

        // Step 3: type
        WebElement el3 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("password")));
        el3.clear();
        el3.sendKeys("secret_sauce");

        // Step 4: click
        wait.until(ExpectedConditions.elementToBeClickable(By.id("login-button"))).click();

        // Step 5: wait
        Thread.sleep(2000);

        // Step 6: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".inventory_item:nth-child(1) .inventory_item_name"))).click();

        // Step 7: wait
        Thread.sleep(1000);

        // Step 8: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("inventory-item.html"));

        // Step 9: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 10: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 11: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 12: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/TC011_product_details.png"));

        // Step 13: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".inventory_details_back_button"))).click();

        // Step 14: wait
        Thread.sleep(1000);

        // Step 15: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("inventory.html"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
