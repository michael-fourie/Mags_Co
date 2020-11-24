# Input Partitioning
## All the possible Inputs for the login_user() function in backend.py

Input 1: A valid user email that belongs to a registered user, a valid password belonging to a user
Input 2: An invalid user email that does not belong to a user, a valid password belonging to a user
Input 3: A valid user email that belongs to a registered user, an invalid password not belonging to a user
Input 4: An invalid user email that does not belong to a user, an invalid passwrod not belonging to a user

Expected Output for 1: A user object belonging to the users email and password
Expected Output for 2: A none type object
Expected Output for 3: A none type object
Expected output for 4: A none type object

The test case test_login_user() t that the correct output is displayed.