# Test Data

```
test_user_register_existing = User(
    email = 'register@test.ca',
    name = 'name_register',
    password = generate_password_hash('name_register'),
    password2 = generate_password_hash('name_register')
    )
    
```
# Testing cases for R2

# GET
##### R2.1 - If the user has logged in, redirect back to the user profile page /
**Mocking**
* mock backend.get_user to return a test_user instance

**Actions**
* open /logout (to invalid any logged-in sessions may exist)<br>
* open /register<br>
* enter test_user's email into element #email<br>
* enter test_user's password into elements #password1 and #password2
* click element input[type="submit"]
* redirect to /login through register
* validate cuttent page contains #welcome header element (login page)
* enter test_user's email into element #email
* enter test user name into element #name
* enter test_user's password into element #password
* click element input[type="submit"]
* open /login again
* validate that current page contains #welcome-header element

##### R2.2 - Otherwise, show the user registration page
**Mocking**
* mock backend.get_user to return a test_user instance (to check that there is no instance)

**Actions**
* open /logout (to invalid any logged-in sessions may exist)<br>
* Ensure there is no new instance of test_user
* open /register
* validate that current page contains register #message element

##### R2.3 - The registration page shows a registration form requesting: email, user name, password, password2
**Mocking**
* no mocking required for this test 

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* Validate that current page contains #message element (on register template page)    
* Validate that page shows all #email, #name, #password1, and #password2 elements on page

# POST  

##### R2.4 - The registration form can be submitted as a POST request to the current URL (/register)
**Mocking**
* mock backend.get_user to submit and return a test_user instance 

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* validate user input type satisfies all registration conditions 
* create instance of test_user
* redirect to /login after sucessful registration
* validate current page contains #welcome-header element (login)

##### R2.5 - Email, password, password2 all have to satisfy the same required as defined in R1
**Mocking**
* mock backend.get_user to submit and return a test_user instance

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* Validate page contains #welcome-header element and no #error-message element, which would
    result from invalid information entry

##### R2.6 - Password and password2 have to be exactly the same
**Mocking**
* mock backend.get_user to return a test_user instance

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* Validate page contains #welcome-header element and not "Passwords do not match" 
error element

#### R2.7 - User name has to be non-empty, alphanumeric-only, and space allowed only if it is not the first or the last character.
**Mocking**
* mock backend.get_user to return a test_user instance
* mock if-statement to verify user's name satisfies all conditions stated above

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* ensure that name is non-empty, if not then return error-message
* ensure that name is alphanumeric only, if not then return error-message
* ensure that name does not have space as first/last character, if so then return
error-message
* Validate page contains #welcome-header element and not any of the error elements
described above


#### R2.8 - User name has to be longer than 2 characters and less than 20 characters.
**Mocking**
* mock backend.get_user to return a test_user instance
* mock if-statement to verify user's name satisfies all conditions stated above

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* ensure that name is longer than 2 characters and less than 20 characters, 
if not then return error message
* Validate page contains #welcome-header element and not any of the error elements
described above

#### R2.9 - For any formatting errors, redirect back to /login and show message '{} format is incorrect.'.format(the_corresponding_attribute)
**Mocking**
* mock backend.get_user to return a test_user instance
* mock if-statements to verify user input satisfies all formatting conditions

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* check to see if all user input is correct by if statements
* if one of the input has formatting error, return corresponding 
error-message to #message element
* Validate that #message element contains error-message 
* redirect back to login

#### R2.10 - If the email already exists, show message 'this email has been ALREADY used'
**Mocking**
* mock backend.get_user to return a test_user instance (registering user)
* mock backend.get_user to return all instances of user
* mock if-statement to go through user email database

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* loop through all instances of user and compare emails to make sure emails are
 not the same
* If user exists, validate page contains "this email has been ALREADY used" #error-message element and redirect to register page

#### R2.11 - If no error regarding the inputs following the rules above, create a new user, set the balance to 5000, and go back to the /login page 
**Test Data**
```
test_user_register_existing = User(
    email = 'register@test.ca',
    name = 'name_register',
    password = generate_password_hash('name_register'),
    password2 = generate_password_hash('name_register'),
    balance = 0
    )
    
```
**Mocking**
* mock backend.get_user to return a test_user instance (registering user)
* mock backend.get_user to return all instances of user
* mock required if-statements to go through all errors specified above

**Actions**
* open /logout (to invalid any logged-in sessions may exist)
* open /register
* enter test user email into element #email
* enter test user name into element #name
* enter test user password1 into element #password1 
* enter test user password into element #password2
* click element input[type="submit"]
* go through all error catching and return #error-message element if any of the 
tests fail
* if successful, create new instance of user and set user balance to 5000
* redirect to /login after sucessful registration
* validate current page contains #welcome-header element (login)

# R7 TESTING

#### R7.1 - Logout will invalid the current session and redirect to the login page. After logout, the user shouldn't be able to access restricted pages.
**Mocking**
* mock backend.get_user to return a test_user instance

**Actions**
* open /logout (to invalid any logged-in sessions may exist) 
* authenticate after redirect to "/" page
* validate  page contains #welcome-header element (successful redirect to login page)



