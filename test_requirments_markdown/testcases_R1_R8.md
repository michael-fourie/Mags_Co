# Test case R1.1 - If the user hasn't logged in, show the login page
### Mocking:
* There is no mocking required for this test
### Actions:
* Open /logout (to invalid any logged-in sessions that may exist)
* Open /login 
* Validate that the current page contains #message element


# Test case R1.2 - the login page has a message that by default says 'please login'
### Mocking:
* There is no mocking required for this test
### Actions
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
* Validate that the current page contains #message element
* Validate that the #message element says 'Please login' and is not empty


## Test case R1.3 - If the user has logged in, redirect to the user profile page
### Test Data:
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions may exist)
* open /login
* enter test_user's email into element #email
* enter test_user's password into element #password
* click element input[type="submit"]
* open /login again
* validate that current page contains #welcome-header element


## Test case R1.4 - The login page provides a login form which requests two fields: email and passwords
### Mocking:
* There is no mocking required for this test
### Actions:
* open /logout (to invalid any logged-in sessions may exist)
* open /login
* validate that the current page contains #email input element
* validate that the current page contains #password input element
* enter test_user's email into element #email
* enter test_user’s password into element #password


## Test case R1.5 - The login form can be submitted as a POST request to the current URL (/login)
### Test Data:
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user’s password into element #password
* validate that element input[type=“submit”] exists
* click element input[type=“submit”]
* validate that current url is /login


## Test case R1.6 - Email and password both cannot be empty
### Mocking:
* No mocking required for this test
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
* click element input[type=“submit”]
* validate that #message element reads 'login failed'


## Test case R1.7 - Email has to follow addr-spec defined in RFC 5322 
### Test Data:
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
*  enter test_user’s email into element #email
*  parse the entered user email using an email parser
*  validate that the local-part contains only upper and lower case latin letters, digits 0 to 9, printable characters, and dots.
*  validate that there is an @ symbol following the local part
*  validate that the domain contains only upper and lower case latin letters, digits 0 to 9, printable characters, and hyphens


## Test case R1.8 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character
### Test Data:
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
*  enter test_user’s password into element #password
*  validate that the password is atleast 6 charachters long
*  validate that the password contains atleast one capital latin letter
*  validate that the password contains atleast two lower case latin letters
*  validate that the password contains atleast one special character


## Test case R1.9 - For any formatting errors, render the login page and show the message 'email/password format is incorrect.'
### Test Data:
test_user = User(
    email='invalid \"email"@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
### Mocking:
* Mock backend.get_user to return a test_user instance

### Actions:
* open /logout (to invalid any logged-in sessions may exist)
* open /login 
* enter test_user’s email into element #email
* enter test_user’s password into element #password
* click element input[type=“submit”]
* validate that #message element reads "email/password format is incorrect"



##  Test case R1.10 - If email/password are correct, redirect to /
## Test Data:
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user’s password into element #password
* click element input[type=“submit”]
* validate that current page contains #welcome-header element



## Test case R1.11 - Otherwise, redict to /login and show message 'email/password combination incorrect'
### Test Data:
incorrect_test_user = User(
    email='test_frontend_notrealemail@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)
### Mocking:
* Mock backend.get_user to return a test_user instance
### Actions:
* open /logout (to invalid any logged-in sessions that may exist)
* open /login
* enter test_user's email into element #email
* enter test_user’s password into element #password
* click element input[type=“submit”]
* validate that #message element reads "email/password combination incorrect"
* validate that url is /login


## Test case R8.1 - For any other requests except the ones above system should return 404 error
### Mocking:
* No mocking required for this test

### Actions:
* open /*
* validate that systems returns 404 error code








