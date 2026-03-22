/*
 * Auto-generated test script from Excel
 * Test Case: TC007 - Complete Checkout Flow
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

public class TestCompleteCheckoutFlow {

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

    @Test(description = "Complete Checkout Flow")
    public void test_complete_checkout_flow() throws Exception {
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
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".inventory_item:nth-child(1) .btn_inventory"))).click();

        // Step 7: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".shopping_cart_link"))).click();

        // Step 8: wait
        Thread.sleep(1000);

        // Step 9: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("cart.html"));

        // Step 10: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 11: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".checkout_button"))).click();

        // Step 12: wait
        Thread.sleep(1000);

        // Step 13: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("checkout-step-one.html"));

        // Step 14: type
        WebElement el14 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("first-name")));
        el14.clear();
        el14.sendKeys("John");

        // Step 15: type
        WebElement el15 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("last-name")));
        el15.clear();
        el15.sendKeys("Doe");

        // Step 16: type
        WebElement el16 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("postal-code")));
        el16.clear();
        el16.sendKeys("12345");

        // Step 17: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".cart_button"))).click();

        // Step 18: wait
        Thread.sleep(1000);

        // Step 19: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("checkout-step-two.html"));

        // Step 20: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 21: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/TC007_checkout_summary.png"));

        // Step 22: click
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector(".cart_button"))).click();

        // Step 23: wait
        Thread.sleep(1000);

        // Step 24: verify_url
        Assert.assertTrue(driver.getCurrentUrl().contains("checkout-complete.html"));

        // Step 25: verify_text
        String text25 = wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("complete-header"))).getText();
        Assert.assertTrue(text25.contains("THANK YOU"), "Expected \"THANK YOU\" but got \"" + text25 + "\"");

        // Step 26: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/TC007_order_complete.png"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
