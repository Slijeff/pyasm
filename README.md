# pyasm
A few days ago I was working on some leetcode problems, and I was wondering how to beat 99% of the people all the time. So a strange thought came up to me, which is to find a way to use assembly in Python.
It's natural since assembly is supposed to be the "fastest" language right? Leetcode only compares your program runtime with other people who are using the same language, so this repo should work... in theroy.

## Conclusion
After playing around with this and testing things, it turns out that Python's interpreter is actually highly optimized. The overhead of allocating a chunck of memory, putting the assembly inside the buffer, and
executing it is too much compare to Python's native way of doing things. The conclusion is to use Python's builtin functions whenever possible, which should yield great performance most of the time.
