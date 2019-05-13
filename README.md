# AutograderApp #
To run this application locally, in the webApp directory run __`python app.py`__.

# Usage #

1. Create a Professor Account 
2. Sign In with the Professor Account
3. Create a Class with a Name
4. Click on the Class and create Assignments
5. Please upload all fields of data
    - Fill in all and use the dropdowns where needed
    - For the date, it should be mm/dd/yyyy
    - Upload files for description, tests, and results
      - Naming Convention for Tests: test1.txt, test2.txt, test3.txt ...
      - Naming Convention for Results: result1.txt, result2.txt, result3.txt ... 
    - Every test file is worth 10 points 
    - Choose Command Line or User Input which specifies if the student's code should take the test file as a command line argument or user input using the cat command
    - The output of test1.txt and the result1.txt will be compared and the output of test2.txt and the result2.txt will be compared and so on ..
    - Our code doesn't classify floating points the same as integers so 4.0 != 4
6. Copy the Class Code in the bottom left of screen with all the assignments for your class
7. Create student accounts
8. Log in with one of them
9. Click add a class and paste the Class Code which was copied before 
10. Click on the class and then an assignment
11. Click the download button to download the description and upload a file to be graded by the autograder
12. Once it is uploaded, the grade will show up
13. Upload the files for all the assignments from the users you created 
14. Then login as a Professor, click on the class you created, and click on each of the assignments to see the grades for each student

# Random Bug #
When you create an assignment as a professor and click the create assignment button, it will route you to the dashboard link. Sometimes this URL is unavailable and you will have to go back to the main page. The assignment is still created, but there is a bug in the routing functionality. 
