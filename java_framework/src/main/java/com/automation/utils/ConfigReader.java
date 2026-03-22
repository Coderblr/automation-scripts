package com.automation.utils;

import java.io.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/**
 * Reads config.ini and provides ${variable} mappings for the KeywordEngine.
 * Testers change config.ini once, and all Excel test cases pick up the values.
 */
public class ConfigReader {

    private static final String CONFIG_PATH = "../config/config.ini";
    private static Properties properties;
    private static Map<String, String> variables;

    static {
        properties = new Properties();
        variables = new HashMap<>();
        loadConfig();
    }

    private static void loadConfig() {
        File configFile = new File(CONFIG_PATH);
        if (!configFile.exists()) {
            configFile = new File("config/config.ini");
        }

        try (BufferedReader reader = new BufferedReader(new FileReader(configFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#") || line.startsWith("[")) continue;

                int eqIdx = line.indexOf('=');
                if (eqIdx > 0) {
                    String key = line.substring(0, eqIdx).trim();
                    String value = line.substring(eqIdx + 1).trim();
                    properties.setProperty(key, value);
                }
            }
        } catch (IOException e) {
            System.err.println("Warning: Could not load config file: " + configFile.getAbsolutePath());
        }

        variables.put("base_url", get("base_url", "http://localhost:3000"));
        variables.put("api_url", get("api_base_url", "http://localhost:8000"));
        variables.put("username", get("test_username", ""));
        variables.put("password", get("test_password", ""));
        variables.put("browser", get("browser_name", "chrome"));

        System.out.println("[Config] base_url  = " + variables.get("base_url"));
        System.out.println("[Config] username  = " + variables.get("username"));
        System.out.println("[Config] browser   = " + variables.get("browser"));
    }

    public static String get(String key) {
        return properties.getProperty(key, "");
    }

    public static String get(String key, String defaultValue) {
        return properties.getProperty(key, defaultValue);
    }

    public static String getBrowser() { return variables.getOrDefault("browser", "chrome"); }
    public static String getBaseUrl() { return variables.getOrDefault("base_url", "http://localhost:3000"); }
    public static String getApiBaseUrl() { return variables.getOrDefault("api_url", "http://localhost:8000"); }
    public static String getUsername() { return variables.getOrDefault("username", ""); }
    public static String getPassword() { return variables.getOrDefault("password", ""); }
    public static boolean isHeadless() { return Boolean.parseBoolean(get("headless", "false")); }
    public static String getExcelPath() { return get("excel_path", "../test_data/test_cases.xlsx"); }

    /**
     * Returns the variable map for ${variable} substitution in Excel test data.
     */
    public static Map<String, String> getVariables() {
        return new HashMap<>(variables);
    }

    /**
     * Resolves ${variable} placeholders in a string using config values.
     * Example: "${base_url}" becomes "https://www.saucedemo.com/"
     */
    public static String resolveVariables(String text) {
        if (text == null || text.isEmpty()) return text;
        for (Map.Entry<String, String> entry : variables.entrySet()) {
            text = text.replace("${" + entry.getKey() + "}", entry.getValue());
        }
        return text;
    }
}
