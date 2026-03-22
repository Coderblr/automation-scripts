/*
 * Auto-generated test script from Excel
 * Test Case: TC002 - Homepage Verification
 * Generated: 2026-03-21 10:30:26
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

public class TestHomepageVerification {

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

    @Test(description = "Homepage Verification")
    public void test_homepage_verification() throws Exception {
        // Step 1: navigate
        driver.get("http://localhost:3000");

        // Step 2: verify_title
        Assert.assertTrue(driver.getTitle().contains("Home"));

        // Step 3: verify_element_present
        Assert.assertTrue(driver.findElements(By.xpath("//nav")).size() > 0, "Element not found: xpath=//nav");

        // Step 4: verify_element_visible
        // TODO: Unknown action "verify_element_visible" - implement manually

        // Step 5: take_screenshot
        File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
        FileUtils.copyFile(screenshot, new File("reports/screenshots/homepage.png"));

    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
