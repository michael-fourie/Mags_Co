## Descriptions on how you modified the template to conduct the testing if any. If

## you propose a different approach than the template, explain how you did that and

## justify why.

## R1: For this set of specifications, the following changes were made

- All of the created test cases follow the template provided by the professor.
- The test cases for R1.1 - R1.11 were implemented to validate the code and
check for any failures
- R1.1: associated with test_not_loggedin
- R1.2: associated with test_login_message
- R1.3: associated with test_logged_in_redirect
- R1.4: associated with test_login_two_fields
- R1.5: associated with test_login_as_post
- R1.6: associated with test_email_password_empty
- R1.7: associated with test_valid_email
- R1.8: associated with test_invalid_password
- R1.9: associated with test_formatting_errors
- R1.10: associated with test_email_password_correct
- R1.11: test_email_password_incorrect

## R2: For this set of specifications, the following changes were made:

- All testing followed template provided by professor
- Created test cases for R2.1-R2.11 to validate code and check for failures.
- Created instance of a registered user to mock the backend - test_register_user.
- R2.1, R2.2, R2.3 created test cases​ ​test_register_has_logged_in, 
test_register_hasnt_logged_in, test_register_page
- No new code added for these test cases
- R2.4: created test case test_register
- R2.4: created test_register_non_match
- R2.1: created test case test_register empty
- R2.2: created test case t​est_register_alnum
- Repaired code in frontend.py that was providing a bug based on logical error of if
statement.
- R2.3: created test case ​test_register_space
- R2.4: created test case ​test_register_name_short
- R2.4: created test case ​test_register_name_long
- Needed to create two subtests for 1) the name being too long
2) the name being too short
- R2.6: created test case ​test_register_format
- R2.7: created test case ​test_register_email_already_used
- R2.8: created test case ​test_register_success

## R3: For this set of specifications, the following changes were made:
- Created test cases for all R3.1-R3.7 to validate code and check for failures
- R3.1: created test case test_not_loggedin
- R3.2: created test case test_show_header
- R3.3: created id tag “user-balance” in index.html for the mock testing of
 test_balance
- R3.4: created id tag “logout-link” in index.html for the mock testing of
test_show_logout
- R3.5: created new variables in id=”tickets” for index.html so that name, price,
quantity, email and date were all displayed. Also added more fields to the mock
instance of test_tickets in test_registration for the frontend. Then used all of the
above to verify in test case test_login_success
- R3.6: created test case test_form_sell and linked with id tags in index.html
- R3.7: created test case test_form_buy and linked with id tags in index.html
- Created test cases for all R3.8-R3.10 and R7.1 and R8.1 to validate code and
 check for failures
- R3.8: created test case test_ticket_sell_form and added id tags in index.html to
differentiate submit buttons, added action to form_sell
- R3.9: created test case test_ticket_buy_form and added id tags in index.html to
differentiate submit buttons, added action to form_buy
- R3.10: created test case test_ticket_update_form and added if tags in index.html

## R7: For this set of specifications, the following changes were made:
- R7.1: created test case test_logout

## R3: For this set of specifications, the following changes were made:
- R8.1: created test case test_unexpected_input and imported requests

Overall the original template was kept and we added our own test cases that mimicked
the examples given. Additionally a few small changes were made to the code such as
logic errors and small bugs but no major change to program structure or the overall
template was changed.

# DETAILED FAILURE REPORT

## R1 FAILURES
| Test Name                | What it was Testing                                       | How Output was  Wrong                                                                                                                | What was Error  in Code                                                                                                          | How You Changed  Error to Fix                                |
|--------------------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| test_logged_in_redirect | If the user has logged  in, redirect to the  user profile | Upon getting the use user  page and checking for the  element “#tickets div h4”,  pytest could not find the  element after 6 seconds | The element ID in  the index.html  did not have the  correct name.                                                               | Changed the name of  the id in the  index.html file          |
| test_logged_in_redirect  | If the user has logged in, redirect to the user profile   | Upon clicking input[type=”submit”], an incorrect password message was being presented                                                | The password checks for passwords to have capital, lower case, and special character, which the test users password did not have | Change the test_users password to pass password requirements |

## R2 FAILURES

| Test Name                        | What it was Testing                                                            | How Output was  Wrong                                                             | What was Error  in Code                                                                                                        | How You Changed  Error to Fix                                 |
|----------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| test_register_space              | User name has spaces allowed only if it is not the first or the last character | Register_post was returning no error string when sending in invalid name strings. | Logical error by writing a full if-elif case for every condition so some of the conditions were missed after lan(password) > 5 | Changed the logic of the validity checking in register_post() |
| test_register_name_short         | User name has to be longer than 2 characters                                   | Register_post was returning no error string when sending in invalid name strings. | Logical error by writing a full if-elif case for every condition so some of the conditions were missed after lan(password) > 5 | Changed the logic of the validity checking in register_post() |
| test_register_name_long          | User name has to be less than 20 characters                                    | Register_post was returning no error string when sending in invalid name strings. | Logical error by writing a full if-elif case for every condition so some of the conditions were missed after lan(password) > 5 | Changed the logic of the validity checking in register_post() |
| test_register_email_already_used | If the email already exists, show message 'this email has been ALREADY used    | Register_post was returning no error string when sending in invalid name strings. | Logical error by writing a full if-elif case for every condition so some of the conditions were missed after lan(password) > 5 | Changed the logic of the validity checking in register_post() |

# R3 FAILURES

| Test Name               | What it was Testing                                                                            | How Output was  Wrong                  | What was Error  in Code                                                                          | How You Changed  Error to Fix                                       |
|-------------------------|------------------------------------------------------------------------------------------------|----------------------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| test_balance            | That the page shows user balance                                                               | The balance didn’t display properly    | No id tag was written for balance                                                                | Wrote an id tag                                                     |
| test_show_logout        | Page shows logout link, pointing to /logout                                                    | The test couldn’t identify logout link | No id tag was written for logout                                                                 | Wrote an id tag                                                     |
| test_login_success      | Page lists all available tickets including info for quantity, email, price and expiration date | It only output name and quantity       | There weren’t variables written for email, price and expiration date                             | Wrote in variables to have email, price and expiration date show up |
| test_ticket_sell_form   | Ticket-selling form can be post to /sell                                                       | Form did not get posted to /sell       | No action was in form ‘form_sell’                                                                | Added action in form_sell to POST form to /sell when submitted      |
| test_ticket_buy_form    | Ticket-buying form can be post to /buy                                                         | Form did not get posted to /buy        | No action was in form ‘form_buy’                                                                 | Added action in form_buy to POST form to /buy when submitted        |
| test_ticket_update_form | Ticket-update form can be post to /update                                                      | Update button did not update           | Did not have unique id for submit button, was getting confused with other submit buttons on page | Added id ‘submit_update’                                            |

# NO OBSERVED FAILURES FOR R7 AND R8



