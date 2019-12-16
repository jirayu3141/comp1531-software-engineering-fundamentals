During this iteration (iter3), our team went over all of our existing codes and identified any design smells. To improve our code and make it more extensible, reusable, maintainable, understandable and testable, we employed the DRY (Don't Repeat Yourself) and KISS (Keep It Simple, Stupid) techniques. This also relates to the Single Responsibility Principle, which states that "every module, function, class should have responsibility for a single piece of functionality". To achieve this, we (1) added many helper functions (stored in the data_structure.py file) which makes our code more readable, and remove existing repetitions (e.g checking validity of email, and password is used in multiple functions); expanding on that, we raised errors in those helper functions, so as not needing to do it repeatedly in the main functions (e.g. getUserFromToken is a helper function that searches the data for user, and if user is not found, it raises an error. That means none of those core functions, that take in token to check user existence, need to raise errors for non-existent user). (2) Simplifying code by minimizing use of nested 'if' statements and loops (3) Removing unnecessary code and removing unused modules. 

Our team also considered switching our database to a class system, which would provide a more structual approach and benefits such as encapsulation, which would prevent unwanted changes in data by restricting its access. However, this would require a lot of time to adopt the object-oriented system into our codes.

Additionally, we put extra effort so as to make our functions cover all cases. For instance, `admin_userpermission()` changes covers the case in which the last owner of slackr would not be allowed to demote himself and `channel_leave()` covers the case for which channel would automatically be deleted when last member of the channel leaves. Finally, we spare ample time at the end of this iteration to refactor our codes. One of the cases which we refactor is that the non case-sensitive case for search function. We check the specification thoroughly in order to make sure that our functions work perfectly with frontend. 

# changelog

7 Nov Fairuz
- Create reset function for dwhich resets user to be an empty list and call it at the beginning of each test so that each test could run individually.
- Change from importing * to only functions that are called.
- Move helper function to data_structure.py so other files can utilise all functions
- Use getData() instead of global data

7 Nov Peter/Sojin
- Fully integrated channel functions with frontend
- Corrected return value for channel list and listall to match frontend requirement
- Modified functions_channel; Created extra helper functions in data_structure.py to minimize nested 'if's and loops and improve style
- Bug fixes

8 Nov Peter
- Changed imports to absolute import

10 Nov Peter
- Added auto save functions using pickles (callable when needed)
- Fixed msg pin/edit bugs

11 Nov Peter
- Added exception handler

12 Nov Sojin and Peter
- Fixed channel bugs
- Fixed bugs in exception handler
- Fixed message/react bugs

13 Nov Peter
- Change datetime object to Sydney time
- Fixed bug in channel/message to only show message that has been sent in the past

14 Nov Peter
- Fixed standup function bugs. Standup functions now are fully working

15 Nov Peter
- Checked that frontend is working for all functions
- Make profile photo download photo from internet and save it locally

16 Nov Sojin, Earth and Peter
- Achieved 100% coverage on all of the funcitons 



