# Slimleaf UI Automation Tools
A sensible approach to fast, scalable, robust UI automation suites in Python

<h2>Principles</h2>

<details><summary><b>Writing Tests Should Not Suck™</b></summary>
<p>

  - If you aren't where you expect to be, the page should tell you.
    - unique locators are checked automatically when navigating to a page
    - `assert blog_page.is_current_page` any time you want to validate manually

  - Element objects should be there when we need them.
    - Slimleaf elements are lazy-loaded, so they will never go stale unless we allow them to.

  - If it's not increasing coverage, you shouldn't have to build or maintain it.
    - Slimleaf switches windows and tabs for you.
    - Slimleaf handles most "waits" for you automatically. "Smart Waits" ensure you aren't waiting a millisecond longer than absolutely necessary during test runs, and avoids broken tests caused by impatient frameworks.
</p>
</details>

<details><summary><b>Testers should be able to add value NOW, not later.</b></summary>
<p>

  - You should not have to learn Selenium in order to add valuable automated tests.
    - A new tester can learn to write valuable automation cases with Slimleaf in less than one hour. Let them worry about architecture later (or never).
    ```
    homepage.go()
    homepage.login_button.click()
    assert homepage.bad_password_alert.is_displayed
    ```
</p>
</details>

<details><summary><b>Solving the same problem twice is foolish and expensive.</b></summary>
<p>

  - Slimleaf's implementation encourages fast, robust, maintainable automation practices across the entire organization
  - Centralized, easy-to-use tools avoid the temptation to implement duplicated one-offs
  - Reusable components ensure the most value for the least amount of code

</p>
</details>

###### Step: 1
pip install slimleaf

###### Step: 2
import slimleaf
