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

    -Class
      +Assignments
      +Students
      +Professor
      +Class Code

    -Assignment
      +Description
      +Due Date
      +Number of resubmissions
      +Run command
      +Tests
      +Results
      +Grade
      +Command Line / User Input
      +Language

General Notes:
  make sure file format for input is right
