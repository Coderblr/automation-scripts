package com.automation.base;

import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

import org.apache.commons.io.FileUtils;

public class BasePage {

    protected WebDriver driver;
    protected WebDriverWait wait;
    protected Actions actions;

    public BasePage(WebDriver driver) {
        this(driver, 20);
    }

    public BasePage(WebDriver driver, int waitTime) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(waitTime));
        this.actions = new Actions(driver);
    }

    private By getBy(String locatorType, String locatorValue) {
        switch (locatorType.toLowerCase()) {
            case "id": return By.id(locatorValue);
            case "name": return By.name(locatorValue);
            case "xpath": return By.xpath(locatorValue);
            case "css": return By.cssSelector(locatorValue);
            case "class": return By.className(locatorValue);
            case "tag": return By.tagName(locatorValue);
            case "link_text": return By.linkText(locatorValue);
            case "partial_link_text": return By.partialLinkText(locatorValue);
            default: throw new IllegalArgumentException("Invalid locator type: " + locatorType);
        }
    }

    // --- Element Finding ---

    public WebElement findElement(String locatorType, String locatorValue) {
        return wait.until(ExpectedConditions.presenceOfElementLocated(getBy(locatorType, locatorValue)));
    }

    public WebElement findClickable(String locatorType, String locatorValue) {
        return wait.until(ExpectedConditions.elementToBeClickable(getBy(locatorType, locatorValue)));
    }

    public WebElement findVisible(String locatorType, String locatorValue) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(getBy(locatorType, locatorValue)));
    }

    // --- Actions ---

    public void click(String locatorType, String locatorValue) {
        findClickable(locatorType, locatorValue).click();
    }

    public void typeText(String locatorType, String locatorValue, String text) {
        WebElement element = findVisible(locatorType, locatorValue);
        element.clear();
        element.sendKeys(text);
    }

    public void clearField(String locatorType, String locatorValue) {
        findVisible(locatorType, locatorValue).clear();
    }

    public void selectDropdown(String locatorType, String locatorValue, String optionText) {
        WebElement element = findVisible(locatorType, locatorValue);
        new Select(element).selectByVisibleText(optionText);
    }

    public void hover(String locatorType, String locatorValue) {
        WebElement element = findVisible(locatorType, locatorValue);
        actions.moveToElement(element).perform();
    }

    public void doubleClick(String locatorType, String locatorValue) {
        WebElement element = findClickable(locatorType, locatorValue);
        actions.doubleClick(element).perform();
    }

    public void rightClick(String locatorType, String locatorValue) {
        WebElement element = findClickable(locatorType, locatorValue);
        actions.contextClick(element).perform();
    }

    // --- Navigation ---

    public void navigateTo(String url) {
        driver.get(url);
    }

    public void refresh() { driver.navigate().refresh(); }
    public void goBack() { driver.navigate().back(); }
    public void goForward() { driver.navigate().forward(); }

    // --- Getters ---

    public String getText(String locatorType, String locatorValue) {
        return findVisible(locatorType, locatorValue).getText();
    }

    public String getAttribute(String locatorType, String locatorValue, String attribute) {
        return findElement(locatorType, locatorValue).getAttribute(attribute);
    }

    public String getTitle() { return driver.getTitle(); }
    public String getCurrentUrl() { return driver.getCurrentUrl(); }

    // --- Verification ---

    public boolean isElementPresent(String locatorType, String locatorValue) {
        try {
            driver.findElement(getBy(locatorType, locatorValue));
            return true;
        } catch (NoSuchElementException e) {
            return false;
        }
    }

    public boolean isElementVisible(String locatorType, String locatorValue) {
        try {
            return driver.findElement(getBy(locatorType, locatorValue)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public void verifyText(String locatorType, String locatorValue, String expected) {
        String actual = getText(locatorType, locatorValue);
        if (!actual.contains(expected)) {
            throw new AssertionError("Text verification failed. Expected: '" + expected + "', Got: '" + actual + "'");
        }
    }

    public void verifyTitle(String expected) {
        String actual = getTitle();
        if (!actual.contains(expected)) {
            throw new AssertionError("Title verification failed. Expected: '" + expected + "', Got: '" + actual + "'");
        }
    }

    public void verifyUrlContains(String expected) {
        String actual = getCurrentUrl();
        if (!actual.contains(expected)) {
            throw new AssertionError("URL verification failed. Expected '" + expected + "' in '" + actual + "'");
        }
    }

    // --- Frames & Windows ---

    public void switchToFrame(String locatorType, String locatorValue) {
        WebElement frame = findElement(locatorType, locatorValue);
        driver.switchTo().frame(frame);
    }

    public void switchToDefaultContent() {
        driver.switchTo().defaultContent();
    }

    public void switchToWindow(int index) {
        List<String> handles = new java.util.ArrayList<>(driver.getWindowHandles());
        if (index < handles.size()) {
            driver.switchTo().window(handles.get(index));
        }
    }

    // --- Alerts ---

    public void acceptAlert() {
        wait.until(ExpectedConditions.alertIsPresent());
        driver.switchTo().alert().accept();
    }

    public void dismissAlert() {
        wait.until(ExpectedConditions.alertIsPresent());
        driver.switchTo().alert().dismiss();
    }

    // --- JavaScript ---

    public Object executeJs(String script, Object... args) {
        return ((JavascriptExecutor) driver).executeScript(script, args);
    }

    public void scrollDown(int pixels) {
        executeJs("window.scrollBy(0, " + pixels + ")");
    }

    public void scrollUp(int pixels) {
        executeJs("window.scrollBy(0, -" + pixels + ")");
    }

    public void scrollToElement(String locatorType, String locatorValue) {
        WebElement element = findElement(locatorType, locatorValue);
        executeJs("arguments[0].scrollIntoView(true);", element);
    }

    // --- Screenshot ---

    public String takeScreenshot(String name) {
        try {
            File dir = new File("../reports/screenshots");
            dir.mkdirs();
            if (name == null || name.isEmpty()) {
                name = "screenshot_" + LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
            }
            File screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE);
            File dest = new File(dir, name + ".png");
            FileUtils.copyFile(screenshot, dest);
            return dest.getAbsolutePath();
        } catch (Exception e) {
            System.err.println("Screenshot failed: " + e.getMessage());
            return null;
        }
    }

    // --- Wait ---

    public void waitSeconds(double seconds) throws InterruptedException {
        Thread.sleep((long) (seconds * 1000));
    }
}
