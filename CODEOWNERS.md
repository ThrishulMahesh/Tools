# Lines starting with '#' are comments.
# Each line is a file pattern followed by one or more owners.

# These owners will be the default owners for everything in the repo.
*       @Indu04

# Order is important. The last matching pattern has the most precedence.
# So if a pull request only touches Python files, only these owners
# will be requested to review.
*.py    @Indu04 @github/py

# You can also use email addresses if you prefer.
docs/*  docs@example.com
