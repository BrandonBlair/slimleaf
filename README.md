# SlimLeaf UI Automation Tools
A sensible approach to fast, scalable, robust UI automation suites in Python

### Principles
- Writing Tests Should Not Suck™
  - Testers should be able to add value NOW, not later.
    - You do not need to understand Selenium to add valuable automated tests
      - Tester can learn to manipulate and validate page objects in less than an hour. They can worry about architecture later (or never) depending on technical aptitude.
      ```
      homepage.go()
      homepage.login_button.click()
      assert homepage.bad_password_alert.is_displayed
      ```
    - If you have spent months teaching someone an over-architected, unintuitive, proprietary automation framework, you have wasted a lot of money on something they:
      1. probably hate using
      2. cannot transfer to any other problem domain
      3. spend all of their time maintaining vs. adding new coverage
    Their productivity will either decline or never manifest, and they will either quit or take a salary for little-to-no ROI.
  - Tests shouldn't break because your framework was impatient.
    - Slimleaf's "smart waits" come baked-in and execute automatically. You focus on writing tests, SlimLeaf will handle the waits for you.
- Page Objects should be small but smart
  - If you aren't where you expect to be, the page should tell you.
    - unique locators are checked automatically when navigating to a page
    - `assert blog_page.is_current_page` any time you want to validate
  - Window and Tab handling come standard
    -
      ```
      blog_page.signup_button.click()
      blog_page.switch_to_newest_window()
      # Continue testing
      ```

  - Element objects should be there when we need them.
    - SlimLeaf elements are lazy-loaded, so they will never go stale unless we allow them to.
  - We should only have to solve the problem once.
    - Reusable components eliminate duplicated code.

###### Step: 1
- pip install slimleaf

###### Step: 2
- import slimleaf
