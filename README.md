# AutograderApp

Session Mangement:
  keep track of userID to send between requests

MongoDB:
  setup collections
    Schemas
    -User
      +ID
      +Name
      +Classes
      +Professor/Student
      +Email Address

    -Class
      +Assignments
      +Students
        - Student IDs
      +Professor ID
      +Class Code

    -Assignment
      +Name
      +Due Date
      +Run command
      +Command Line / User Input
      +Language
      +Description
      +Tests
      +Results

    -Submission
      +
General Notes:
  make sure file format for input is right
