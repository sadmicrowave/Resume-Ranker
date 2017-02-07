

Contribute to Resume Ranker
=============

Thank you for your interest in contributing to Resume Ranker. This guide details how to contribute to Resume Ranker in a way that is efficient for everyone.


### Security vulnerability disclosure
Please report suspected security vulnerabilities in private to `corey.m.farmer@gmail.com`. **Please do NOT create publicly viewable issues for suspected security vulnerabilities.**

### Closing policy for issues and merge requests
Resume Ranker is an open source project and the capacity to deal with issues and merge requests is limited. Out of respect for our limited resouces, issues and merge requests not in line with the guidelines listed in this document may be closed without notice.

Please treat the developers and fellow contributors with courtesy and respect, it will go a long way towards getting your issue resolved.

Issues and merge requests should be in English and contain appropriate language for audiences of all ages.

### I want to contribute!

If you want to contribute to Resume Ranker, but are not sure where to start, navigate to the issues tab and peruse until your heart is content.  Many of the issues will be labeled with the `feature request` tag denoting the context of enhancement rather than issue or bug.  This is a great place for anyone to start.


### Issue tracker guidelines

Search the issue tracker for similar entries before submitting your own, there's a good chance somebody else had the same issue or feature proposal.  Show your support with an award emoji and/or join the discussion.

Please submit bugs using the `Bug` issue tag provided on the issue tracker, and feature requests with the `Feature Request` issue tag.


### Merge request guidelines

If you can, please submit a merge request with the fix or improvements including tests. If you don't know how to fix the issue but can write a test that exposes the issue we will accept that as well. In general bug fixes that include a regression test are merged quickly while new features without proper tests are least likely to receive timely feedback. The workflow to make a merge request is as follows:

1. Fork the project into your personal space on GitHub.com
2. Create a feature branch, branch away from master
3. Write tests and code
4. Generate a changelog entry with bin/changelog
5. If you have multiple commits please combine them into one commit by squashing them
6. Push the commit(s) to your fork
7. Submit a merge request (MR) to the master branch
8. The MR title should describe the change you want to make
9. The MR description should give a motive for your change and the method you used to achieve it.
10. Link any relevant issues in the merge request description and leave a comment on them with a link back to the MR
11. Be prepared to answer questions and incorporate feedback even if requests for this arrive weeks or months after your MR submission

Please keep the change in a single MR as small as possible. If you want to contribute a large feature think very hard what the minimum viable change is. Can you split the functionality? Can you do part of the refactor? The increased reviewability of small MRs that leads to higher code quality is more important to us than having a minimal commit log. The smaller an MR is the more likely it is it will be merged (quickly). After that you can send more MRs to enhance it. 

For examples of feedback on merge requests please look at already closed merge requests.  Please ensure that your merge request meets the contribution acceptance criteria.

When having your code reviewed and when reviewing merge requests please take the code review guidelines into account.



### Contribution acceptance criteria

1. The change is as small as possible
2. Include proper tests and make all tests pass (unless it contains a test exposing a bug in existing code). Every new class should have corresponding unit tests, even if the class is exercised at a higher level, such as a feature test.
3. Your MR initially contains a single commit (please use git rebase -i to squash commits)
4. Your changes can merge without problems (if not please rebase if you're the only one working on your feature branch, otherwise, merge master)
5. Does not break any existing functionality
6. Fixes one specific issue or implements one specific feature (do not combine things, send separate merge requests if needed)
7. Keeps the Resume Ranker code base clean and well structured
8. Contains functionality we think other users will benefit from too
9. Changes after submitting the merge request should be in separate commits (no squashing). If necessary, you will be asked to squash when the review is over, before merging.
10. It conforms to the style guides and the following:
	11.	If your change touches a line that does not follow the style, modify the entire line to follow it. This prevents linting tools from generating warnings.
	12. Don't touch neighbouring lines. As an exception, automatic mass refactoring modifications may leave style non-compliant.
11. If the merge request adds any new libraries (gems, JavaScript libraries, etc.), they should conform to our Licensing guidelines. See the instructions in that document for help if your MR fails the "license-finder" test with a "Dependencies that need approval" error.



### Definition of done

If you contribute to Resume Ranker please know that changes involve more than just code. We have the following definition of done. Please ensure you support the feature you contribute through all of these steps.

1. Description explaining the relevancy (see following item)
2. Working and clean code that is commented where needed
3. Unit and integration tests that pass
4. Documented in the /documentation directory
5. Changelog entry added
6. Reviewed and any concerns are addressed
7. Merged by the project lead
8. Community questions answered
9. Answers to questions radiated (in docs/wiki/etc.)