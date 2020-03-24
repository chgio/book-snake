Giorgio Ciacchella  | March 2020
---                 | ---
 x	            | CS-1P

# CS-1P Assessed Exercise


### Foreword:
In accordance with common-sense good coding practices, a copious number of comments was scattered throughout the files, which describe all sorts of comment-worthy information about the functioning of the program.

This includes:
* an introductory description of the functions' purpose;
* some basic information about the input and output data structures;
* a general walkthrough of the control and data flows;
* any other notable remark.

I genuinely hope that, if this file didn't exist, or was for any reason lost or corrupted, the comments would be thorough and clear enough to provide a sufficiently satisfactory answer to the following questions.



# 1. Describe any complex data structures you used and explain why you think they are suitable.
---

When deciding the appropriate structures for capturing the data, I focused on staying consistent with the pattern lined out by the input files, and on foreseeing what structures would be most appropriate for making the code that applies the operations and algorithms as clean as possible.

After a thorough thought process and a rough sketch of the algorithm's outline, I settled on the following data structures:
```
books = [
    (author, title),
    ...]
```
`books:`            a **list** of **string, string tuples,** since:
*   it's fundamental to maintain the order the books come in the `books.txt` file;
*   author and title don't have to be associated in a "lookup" fashion -- there's no need to get the author knowing the title, or vice versa: author and title will always come together;
*   this is simple data, with simple relationship with its components, other data and the algorithms that manipulate it, so a simple data structure intuitively seems the most appropriate.

```
ratings = {
    user:
    (rating, ...),
    ...}
```
`ratings:`          a **dictionary** of **strings** that map to **integer sequence tuples,** since:
*   as it stands, ratings have no meaningful order;
*   there's a need for mapping each user to their ratings;
*   again, this is relatively simple data, with relatively simple relationships with its components, other data and the algorithms that manipulate it, so this level of complexity seems the most appropriate.

Concerning the `ratings,` I also came up with a possible metric related to users: a **rating index,** which would basically act as a **meta-recommendation.**

This index would simply be *the sum of the absolute values of all the ratings for each user,* and would roughly represent the "polarity" level of any given user: it would be bigger for users who have rated many books and with "extreme" ratings -- like: `(5, -3, 0, 3, -5, 1)` -- while smaller for users who have rated few books and with "average" ratings -- like: `(1, 0, -3, 0, 0)` -- and could be printed out along each recommending user's similarity score to convey a sort of "confidence" in the recommendation.      
It would ideally be calculated for each user upon reading from the `ratings.txt` file, and stored in a tuple along with the username for at-a-glance access:
```
ratings = {
    (user, rating_index):
    (rating, ...),
    ...}
```
This may or may not have been actually implemented in the final revision of the program -- this file was written with time for more possible revisions ahead. Still, regardless of the implementation stage of this idea, I feel like it's a significant detail concerning the data structures involved in the program's operation.

```
recommendations = {
    (user, score):
    [
        (book,
        rating),
        ...],
    ...}
```
`recommendations:`  a **dictionary** of **string, integer tuples** that map to **lists** of **integer, integer tuples,** since:
*   this is an internal data structure, as it is created and exhausted without any I/O and only as a means of communication between functions;
*   its only purpose is to fully and extensively encapsulate all the information about the recommendations as computed by the algorithm, and ready for a meaningful and good-looking print;
*   its main use case is looking up the ordered list of recommendations from the user.

There are some more elementary data structures, which I'll only briefly mention due to their trivial nature:
```
new_ratings = (rating, ...)
random_recommendations = [book, ...]
scores = [(user, score), ...]
```


# 2. How did you break down the problem into sub-problems? Explain the sub-problems and explain how they are organized in recommendations.py.
---

The problem naturally presented itself in three main sub-problems:
*   input/output;
*   core algorithm;
*   user interface.

#### INPUT/OUTPUT
The input/output section revolves around reading from input files, namely `books.txt` and `ratings.txt`, and writing to output files, namely `output-{user}.txt.`

The manipulation of input files is entirely done by three functions:
*   `read_books():`         simply reads from `books.txt` and returns the `books` structure containing the data from the file;
*   `read_ratings():`       reads the ratings from `ratings.txt` and returns the `ratings` structure with the data from the file;
*   `write_ratings():`      additionally, this function is responsible of writing new users' ratings to `ratings.txt.`
On the other hand, the manipulation of output files is entirely done by just two functions:
*   `printer():`            takes as argument a `recommendations` data structure from the core algorithm and nicely prints out all the information it contains to `output-{user}.txt;`
*   `random_printer():`     takes as argument a `r_recommendations` data structure from the random recommendator and nicely prints out its information to `output-{user}.txt.`

#### CORE ALGORITHM
The `recommend()` algorithm is the hearth of the program, as it handles making the book recommendations and thus connects all the input data to the output structure.

In order to operate properly, it needs a handful of helper functions:
*   `dprod():`                  simply takes as arguments two ratings vectors and calculates the dot product between them;
*   `compute_similarity():`     wraps up the `dprod()` function to take as arguments two users and look them up in the `ratings` structure;
*   `compute_sorted_scores():`  further wraps up the `compute_similarity()` function to only take as arguments one user and the `ratings` structure and compute all similarity scores for a given user and sort them to return the `scores` structure;
*   `random_recommend():`       this alternative function makes the recommendations in case of a `rating_index` of `0;`
*   `rating_index():`           additionally, this function takes care of calculating the `rating_index` value hinted to above.

#### USER INTERFACE
All interactions with the user are entirely handled by a **Command-Line Interface,** which is represented by two main functions:
*   `rater():`  asks the new user to rate a percentage of the books, and returns this data in the `new_ratings` structure;
*   `wrap():`   as the name suggests, wraps everything up in one single package, which handles the bulk of user interaction and the fundamental connections between the functions that underpin the program.


# 3. Are there any parts of your code that you think are difficult to understand? If yes, explain them here.
---

One of the least clear parts of my code is quite probably the "type-finding" section in the `rater` function, which prints a type-based error message upon invalid user input:
```
try:
    int(raw)
            # int
except ValueError:
    try:
        float(raw)
            # float
    except ValueError:
            # string
```
This effectively retraces a nested `if - else` structure, only substituting `try` and `except` to `if` and `else` to sift through the possible common invalid types the user could have input, naturally starting from a string:
*   first, try casting the string into an `int:`
    *   if it succeeds, that's an integer;
    *   if it fails, try casting it into a `float:`
        *   if it succeeds, that's a floating point number;
        *   if it fails, that's still a string, which can't be cast into any other basic type.
Quite counter-intuitively, this is the only pattern that makes the recognition possible, as trying to first cast it into a `float` to then branch to `int` and `string` would result in all *numbers* ending up as *integers,* as a `float` can always be truncated and cast into an `int.`

Slightly anticipating the next point, another peculiar piece of code is represented by the recurring "continuous-prompt" sections, which repeatedly catch exceptions in asking the user to specify an input over a default:
```
while True:
    raw = input(...)
    if if len(raw) == 0 or raw[0] == 'n':
        break
    else:
        try:
            int(raw)
            break
        except ValueError:
            continue
```
While the somewhat convoluted control flow involved in this could seemingly lack robustness, all the branches that make it up are *mutually exclusive:*
*   the input either satisfies the `if` clause -- meaning the default option has been accepted -- and therefore the loop is broken;
*   or it doesn't, in which case it either satisfies the `try` trial -- meaning a valid, non-default option has been input -- and therefore the loop is broken;
*   or, again, it doesn't -- meaning an invalid option has been specified -- and threrfore the loop should continue asking the user for input.
In most of the cases where this pattern is applied, I've chosen not to include the aforementioned "type-finding" section to spare some non-fundamental complexity, but it could be perfectly implemented for even more consistency in delivering useful error messages.


# 4. Which possible errors could occur and how have you handled them? Explain whether you have used exception handling or defensive programming and use examples if you like.
---

The general scheme I followed for error handling in this scenario was the following.

The bulk of errors is clearly represented by user input as we, as humans, have this curious tendency to explore outside of the boundaries of what's allowed called free will; which, on the other hand, machines lack -- perhaps for the moment, who knows.
But that's another topic.       
Such errors should be handled in a "soft", more defensive manner: that is to say, without raising any flow-breaking errors, which would cause the program to stop running.      
Instead, I tried my best to handle them by simply catching the exceptions with one or more `try - except` statements, and encapsulating all this process in a `while` loop in order to repeatedly ask the user for appropriate input.

Another kind of user-related "error" is introduced by the adoption of thresholds in the recommendations algorithm: as both the recommended book rating and the recommending user's similarity score can be set to a minimum, it is possible that the required number of recommendations exceeds such thresholds.        
Despite these events leading to an unfulfillment of the user's request, they constitute neither a flow-breaking error nor an invalid user input; rather, they simply represent an overly ambitious request, which can't be fulfilled by the algorithm with its current data: as such, they're very "softly" treated by simply halting the algorithm's iteration, printing out a warning message, and resuming operation.

Notable exceptions to this pattern are the functions which read from the input files, `read_books()` and `read_ratings(),` and the `dprod()` function, responsible for computing the dot product between two ratings vectors.
In the first case, I decided to ripple up the "hard" `FileNotFoundError` raised if the input files are unreachable, for two main reasons:
*   The functions are called immediately upon starting the program, which would vanify the benefits of not interrupting its execution;
*   No user input would be useful towards fixing that error, as an OS-level action is required.
Likewise, in the second case, since the dot product operation is only defined between two vectors of the same size, my decision to `raise` a "hard" `ValueError` instead of "softer" methods was backed by similar reasons:
*   The function is located quite deep in the traceback call stack, which would make rippling up the interruption quite inconvenient;
*   The only thing that could cause such an error is some kind of tampering with the `ratings.txt` file, which is not included in the expected interaction with the user -- as such, asking them for another input would be useless.


Across all these cases, in accordance with basic HCI usability principles, I tried my best to make the error messages -- whether "soft" `print` statements or "hard" `Error` throws -- as meaningful and excplicit as possible about the reason they were raised and any possible fixes.
