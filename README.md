Over the course of AoC 2024, I started using networkx and numpy more.
I also experimented with numba and cython for c-like performance. They each have their
pros and cons, but I would be more likely to reach for numba before cython in the future.

I was able to achieve the same order of magnitude improvement with numba and cython,
but tuning cython required a lot of cython knowledge and cython syntax. numba did complain
when it couldn't jit without falling back to python, so it was easier to ensure I was getting
the best performance. And I could write idiomatic python. AoC doesn't usually require passing
around complex objects, but if I was going to try to accelerate a more complex setup, I might
explore maturin and pyO3 so I could use rust.

The hardest problem was day 24 part 2. I had to look at
https://gitlab.com/0xdf/aoc2024/-/blob/main/day24/day24.py?ref_type=heads
in order to figure it out.
