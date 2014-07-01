Bugs
====
The following are the known bugs.

Auto Grader:
---
1. Execution via the safeexec is not working. Throws the error `setgroups failed`. Consequently the safe_execute() function of the class [ComandExecutor](./evaluate/utils/executor.py) has been modified to call run() directly. See the comments in the safe_execute() function and change the function accordingly.
2. While creating outputs from the solution code during creation of testcases, the resource limits are being set to default values. Ideally we should retrieve the SafeExec object for the testcase and return the appropriate resource limits. Check the comments in the function get_resource_limit() of the class [CreateOutput](./assignments/assignments_utils/create_output.py).

Bodhi Tree:
---
1. The course addition interface is not working. As a result of this we need to add some dummy entries during the setup of the server to get some courses working. Please correct the add_courses view.
