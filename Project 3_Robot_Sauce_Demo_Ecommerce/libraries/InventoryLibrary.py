import random
import time
from selenium.webdriver.common.by import By
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class InventoryLibrary:

    def __init__(self):
        # Initialize SeleniumLibrary and prepare storage for selected products

        self.seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
        self.selected_products = []
        print(" InventoryLibrary loaded successfully.")

    @keyword(name="Wait Until Inventory Page Is Loaded")
    def wait_until_inventory_page_is_loaded(self):
        # Wait for inventory list to be visible, confirming page load

        self.seleniumlib.wait_until_element_is_visible("class=inventory_list", timeout="10s")
        BuiltIn().log(" Inventory page loaded successfully.", level="INFO")

    @keyword(name="Select Random Products")
    def select_random_products(self, count=4):
        # Randomly select 'count' products from the inventory list

        driver = self.seleniumlib.driver
        cards = driver.find_elements(By.CLASS_NAME, "inventory_item")
        selected = random.sample(cards, count)
        self.selected_products = []

        # Extract name and price for each selected product
        for card in selected:
            name = card.find_element(By.CLASS_NAME, "inventory_item_name").text
            price = card.find_element(By.CLASS_NAME, "inventory_item_price").text
            self.selected_products.append((name, price, card))

        BuiltIn().log(f" Selected {count} random products.", level="INFO")

    @keyword(name="Log Selected Product Details")
    def log_selected_product_details(self):
        # Log each selected product's name and price for traceability

        for idx, (name, price, _) in enumerate(self.selected_products, start=1):
            BuiltIn().log(f"{idx}. Product: {name} | Price: {price}", level="INFO")

    @keyword(name="Capture Screenshot Of Selected Products")
    def capture_screenshot_of_selected_products(self, filename):
        # Save screenshot of current inventory view for visual validation

        driver = self.seleniumlib.driver
        driver.save_screenshot(f"screenshots/{filename}")
        BuiltIn().log(f" Screenshot saved: screenshots/{filename}", level="INFO")

    @keyword(name="Add Selected Products To Cart And Validate")
    def add_selected_products_to_cart_and_validate(self):
        # Add selected products to cart and validate cart badge count

        driver = self.seleniumlib.driver
        cart_icon_selector = "class=shopping_cart_badge"

        for idx, (_, _, card) in enumerate(self.selected_products, start=1):
            try:
                add_button = card.find_element(By.TAG_NAME, "button")
                add_button.click()
                BuiltIn().log(f" Added product {idx} to cart.", level="INFO")
            except Exception as e:
                BuiltIn().log(f" Failed to add product {idx}: {str(e)}", level="ERROR")
                raise

        # Validate cart badge reflects correct item count

        self.seleniumlib.wait_until_element_is_visible(cart_icon_selector, timeout="5s")
        count_text = self.seleniumlib.get_text(cart_icon_selector)
        expected_count = str(len(self.selected_products))

        if count_text != expected_count:
            BuiltIn().log(f" Cart count mismatch: expected {expected_count}, got {count_text}", level="ERROR")
            raise AssertionError(f"Cart count mismatch: expected {expected_count}, got {count_text}")

        BuiltIn().log(f" Cart icon shows correct count: {count_text}", level="INFO")

    @keyword(name="Validate Cart Contents Against Selected Products")
    def validate_cart_contents_against_selected_products(self):
        # Navigate to cart and validate that selected products are present

        driver = self.seleniumlib.driver
        self.seleniumlib.click_element("class=shopping_cart_link")
        self.seleniumlib.wait_until_page_contains_element("class=cart_item", timeout="5s")

        # Extract product details from cart
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        cart_details = [
            (item.find_element(By.CLASS_NAME, "inventory_item_name").text,
             item.find_element(By.CLASS_NAME, "inventory_item_price").text)
            for item in cart_items
        ]

        # Compare with previously selected products
        selected_details = [(name, price) for name, price, _ in self.selected_products]
        mismatches = [expected for expected in selected_details if expected not in cart_details]

        if mismatches:
            BuiltIn().log(f" Mismatched items in cart: {mismatches}", level="ERROR")
            raise AssertionError(f"Cart validation failed. Missing or incorrect items: {mismatches}")

        BuiltIn().log(" Cart contents match selected products.", level="INFO")

    @keyword(name="Complete Checkout And Validate Order")
    def complete_checkout_and_validate_order(self):
        # Complete the checkout flow and validate order confirmation

        driver = self.seleniumlib.driver

        # Step 1: Navigate to cart and initiate checkout
        self.seleniumlib.click_element("class=shopping_cart_link")
        self.seleniumlib.wait_until_element_is_visible("id=checkout", timeout="5s")
        self.seleniumlib.click_element("id=checkout")

        # Step 2: Fill in user details
        self.seleniumlib.input_text("id=first-name", "Rajesh")
        self.seleniumlib.input_text("id=last-name", "C")
        self.seleniumlib.input_text("id=postal-code", "600119")
        self.seleniumlib.click_element("id=continue")

        # Step 3: Capture order summary screenshot
        self.seleniumlib.wait_until_element_is_visible("class=summary_info", timeout="5s")
        driver.save_screenshot("screenshots/order_summary.png")
        BuiltIn().log(" Screenshot saved: screenshots/order_summary.png", level="INFO")

        # Step 4: Finish order and confirm success
        self.seleniumlib.click_element("id=finish")
        self.seleniumlib.wait_until_page_contains("Thank you for your order!", timeout="5s")
        BuiltIn().log(" Order completed and confirmation message received.", level="INFO")

    @keyword(name="Validate Product Sorting")
    def validate_product_sorting(self, sort_option):
        # Validate sorting behavior based on selected dropdown option

        driver = self.seleniumlib.driver

        # Step 1: Apply sorting option
        self.seleniumlib.select_from_list_by_label("class=product_sort_container", sort_option)
        BuiltIn().log(f" Selected sort option: {sort_option}", level="INFO")
        self.seleniumlib.wait_until_page_contains_element("class=inventory_item", timeout="5s")

        # Step 2: Extract product names and prices
        cards = driver.find_elements(By.CLASS_NAME, "inventory_item")
        names = [card.find_element(By.CLASS_NAME, "inventory_item_name").text for card in cards]
        prices = [float(card.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", "")) for card in cards]

        # Step 3: Validate sorting logic
        if sort_option == "Price (low to high)":
            if prices != sorted(prices):
                raise AssertionError(" Products are not sorted by price (low to high).")
            BuiltIn().log(" Products sorted by price (low to high).", level="INFO")

        elif sort_option == "Name (Z to A)":
            if names != sorted(names, reverse=True):
                raise AssertionError(" Products are not sorted by name (Z to A).")
            BuiltIn().log(" Products sorted by name (Z to A).", level="INFO")

        else:
            BuiltIn().log(f" Sort validation not implemented for: {sort_option}", level="WARN")

    @keyword(name="Reset App State And Validate")
    def reset_app_state_and_validate(self):
        # Reset app state and validate that cart and product buttons are cleared
        driver = self.seleniumlib.driver

        # Step 1: Open side menu and trigger reset
        self.seleniumlib.click_element("id=react-burger-menu-btn")
        self.seleniumlib.wait_until_element_is_visible("id=reset_sidebar_link", timeout="5s")
        self.seleniumlib.click_element("id=reset_sidebar_link")
        BuiltIn().log(" Reset App State triggered.", level="INFO")

        # Step 2: Refresh page to reflect reset
        driver.refresh()
        self.seleniumlib.wait_until_page_contains_element("class=inventory_item", timeout="5s")

        # Step 3: Validate cart badge is cleared
        cart_badge_selector = "class=shopping_cart_badge"
        is_badge_visible = BuiltIn().run_keyword_and_return_status("Element Should Be Visible", cart_badge_selector)

        if is_badge_visible:
            count = self.seleniumlib.get_text(cart_badge_selector)
            if count != "":
                raise AssertionError(f" Cart not cleared. Badge still shows: {count}")
        else:
            BuiltIn().log(" Cart badge is no longer visible — cart is cleared.", level="INFO")

        # Step 4: Validate all product buttons reset to "Add to cart"
        product_buttons = self.seleniumlib.get_webelements("xpath=//div[@class='inventory_item']//button")
        for idx, button in enumerate(product_buttons, start=1):
            label = button.text.strip().lower()
            BuiltIn().log(f" Product {idx} button label: {label}", level="DEBUG")
            if "add to cart" not in label:
                raise AssertionError(f" Product {idx} button not reset: {label}")
        BuiltIn().log(" All product buttons reset to 'Add to cart'.", level="INFO")